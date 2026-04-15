from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
import torchaudio
import numpy as np
import torch
from torchvision import transforms
import random
import uuid
import librosa
import glob

from pathlib import Path
from apps.audio_detector.forms import UploadAudioForm, DetectorForm, DeleteForm
from sqlalchemy.exc import SQLAlchemyError
from apps.app import db
from apps.crud.models import User
from apps.audio_detector.models import UserAudio, UserAudioTag
from apps.audio_detector.audio_model import network, resblock_v1, mfm
from flask_login import current_user, login_required

dt = Blueprint("audio_detector", __name__, template_folder="templates")
base_dir = Path(__file__).resolve().parent

@dt.route("/")
def index():
    user_audios = (
        db.session.query(User, UserAudio)
        .join(UserAudio)
        .filter(User.id == UserAudio.user_id)
        .all()
    )
    
    user_audio_tag_dict = {}
    for user_audio in user_audios:
       
        user_audio_tags = (
            db.session.query(UserAudioTag)
            .filter(UserAudioTag.user_audio_id == user_audio.UserAudio.id)
            .all()
        )
        user_audio_tag_dict[user_audio.UserAudio.id] = user_audio_tags

    
    detector_form = DetectorForm()
    
    delete_form = DeleteForm()

    return render_template(
        "audio_detector/index.html",
        user_audios=user_audios,
        
        user_audio_tag_dict=user_audio_tag_dict,
        
        audio_detector_form=detector_form,
        delete_form=delete_form
        
    )

@dt.route("/audios/<path:filename>")
def audio_file(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)


@dt.route("/upload", methods=["GET", "POST"])

@login_required
def upload_audio():
    
    form = UploadAudioForm()
    if form.validate_on_submit():
        
        file = form.audio.data

       
        ext = Path(file.filename).suffix
        audio_uuid_file_name = str(uuid.uuid4()) + ext

        
        audio_path = Path(current_app.config["UPLOAD_FOLDER"], audio_uuid_file_name)
        file.save(audio_path)

        
        user_audio = UserAudio(user_id=current_user.id, audio_path=audio_uuid_file_name)
        db.session.add(user_audio)
        db.session.commit()

        return redirect(url_for("audio_detector.index"))
    return render_template("audio_detector/upload.html", form=form)

@dt.route("/audios/delete/<string:audio_id>", methods=["POST"])
@login_required
def delete_audio(audio_id):
    try:
        
        db.session.query(UserAudioTag).filter(
            UserAudioTag.user_audio_id == audio_id
        ).delete()

        
        db.session.query(UserAudio).filter(UserAudio.id == audio_id).delete()

        db.session.commit()
    except Exception as e:
        flash("音声削除処理でエラーが発生しました。")
        
        current_app.logger.error(e)
        db.session.rollback()
    return redirect(url_for("audio_detector.index"))








class NormalizeMel:
  def __init__(self, mean, std, eps=1e-6):
    self.mean = mean
    self.std = std
    self.eps = eps

  def __call__(self, x):
    return (x - self.mean) / (self.std + self.eps)


stats = torch.load(Path(base_dir, "cmvn.pt"))
mean = stats["mean"]
std = stats["std"]
transform = transforms.Compose([NormalizeMel(mean, std)])


model = network(resblock_v1, [2,2,2,2])
checkpoint = torch.load(Path(base_dir, "best_model.pt"),map_location=torch.device('cpu'), weights_only=False)
model.load_state_dict(checkpoint['model_state_dict'])
threshold = checkpoint['threshold']
model.eval() 



def audiodetect(target_audio_path):
    
    


    mel_transform = torchaudio.transforms.MelSpectrogram(
        sample_rate = 16000,
        n_fft = 400,
        hop_length = 160,
        n_mels = 80
    )
    
    db_transform = torchaudio.transforms.AmplitudeToDB()

    waveform, sr = torchaudio.load(target_audio_path, backend="soundfile")
    
    if sr != 16000:
        waveform = torchaudio.functional.resample(waveform, orig_freq=sr, new_freq=16000)

    mel = mel_transform(waveform)

    log_mel = db_transform(mel)

    
    log_mel = transform(log_mel)

    log_mel = log_mel.unsqueeze(0)

    
    
    with torch.no_grad():
     outputs = model(log_mel)

     probs = torch.softmax(outputs, dim = 1)
     prob1 = probs[:, 1].numpy()
  
     prediction = (prob1 >= threshold).astype(int)
    
    if prediction == 1:
        tag = "Real"
    else:
        tag = "Fake"
    
    return tag







    


@dt.route("/detect/<string:audio_id>", methods=["POST"])

@login_required
def detect(audio_id):
    
    user_audio = db.session.query(UserAudio).filter(UserAudio.id == audio_id).first()
    if user_audio is None:
        flash("音声分類対象の画像が存在しません。")
        return redirect(url_for("audio_detector.index"))

    
    target_audio_path = Path(current_app.config["UPLOAD_FOLDER"], user_audio.audio_path)
    
    tag  = audiodetect(target_audio_path)

    try:
        
        user_audio_tag = UserAudioTag(
            user_audio_id=user_audio.id,
            tag_name=tag
        )
        db.session.add(user_audio_tag)
        
        
        user_audio.is_detected = True
        
       
        db.session.commit()
        
    except Exception as e:
        flash("音声分類処理でエラーが発生しました。")
        
        db.session.rollback()
        current_app.logger.error(e)
        return redirect(url_for("audio_detector.index"))
        
    return redirect(url_for("audio_detector.index"))




@dt.errorhandler(404)
def page_not_found(e):
    return render_template("detector/404.html"), 404