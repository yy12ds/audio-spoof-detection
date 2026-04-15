from flask_wtf.file import FileAllowed, FileField, FileRequired
from flask_wtf.form import FlaskForm
from wtforms.fields.simple import SubmitField

class UploadAudioForm(FlaskForm):

    audio = FileField(
        validators=[
            FileRequired("音声ファイルを指定してください。"),
            FileAllowed(["wav", "mp3", "flac"])
        ]
    )
    submit = SubmitField("アップロード")

class DetectorForm(FlaskForm):
    submit = SubmitField("検知")

class DeleteForm(FlaskForm):
    submit = SubmitField("削除")