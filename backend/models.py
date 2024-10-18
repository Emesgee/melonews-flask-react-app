from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # One-to-many relationship with FileUpload
    uploads = db.relationship('FileUpload', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class FileType(db.Model):
    __tablename__ = 'file_types'
    filetypeid = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(50), nullable=False, unique=True)
    allowed_extensions = db.Column(db.String(255), nullable=False)  # Add this field


    def __repr__(self):
        return f'<FileType {self.type_name}>'

class FileUpload(db.Model):
    __tablename__ = 'file_uploads'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=True)
    tags = db.Column(db.String(255), nullable=True)
    subject = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(255), nullable=True)
    country = db.Column(db.String(255), nullable=True)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign key to User
    user_id = db.Column(db.Integer, db.ForeignKey('users.userid'), nullable=False)

    # Foreign key to FileType
    file_type_id = db.Column(db.Integer, db.ForeignKey('file_types.filetypeid'), nullable=False)
    
    def __repr__(self):
        return f'<File {self.filename} of type {self.file_type.type_name}>'
# InputTemplate table
class InputTemplate(db.Model):
    __tablename__ = 'input_templates'
    templateid = db.Column(db.Integer, primary_key=True)
    template_type = db.Column(db.String(50), nullable=False)
    template_description = db.Column(db.Text)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<InputTemplate {self.template_type}>'

# OutputTemplate table
class OutputTemplate(db.Model):
    __tablename__ = 'output_templates'
    templateid = db.Column(db.Integer, primary_key=True)
    template_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<OutputTemplate {self.template_type}>'

# Searches table
class Search(db.Model):
    __tablename__ = 'searches'
    searchid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('users.userid'), nullable=False)
    templateid = db.Column(db.Integer, db.ForeignKey('input_templates.templateid'), nullable=False)
    date_searched = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    template_description = db.relationship('InputTemplate', backref='searches', lazy=True)
    user = db.relationship('User', backref='searches', lazy=True)

    def __repr__(self):
        return f'<Search {self.searchid}>'

# Inputs table
class Input(db.Model):
    __tablename__ = 'inputs'
    inputid = db.Column(db.Integer, primary_key=True)
    searchid = db.Column(db.Integer, db.ForeignKey('searches.searchid'), nullable=False)
    keyword = db.Column(db.String(255), nullable=False)
    filters = db.Column(db.JSON)
    date_input = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    templateid = db.Column(db.Integer, db.ForeignKey('input_templates.templateid'), nullable=False)

    search = db.relationship('Search', backref='inputs', lazy=True)
    template = db.relationship('InputTemplate', backref='inputs', lazy=True)

    def __repr__(self):
        return f'<Input {self.inputid}>'

# Outputs table
class Output(db.Model):
    __tablename__ = 'outputs'
    outputid = db.Column(db.Integer, primary_key=True)
    searchid = db.Column(db.Integer, db.ForeignKey('searches.searchid'), nullable=False)
    filetypeid = db.Column(db.Integer, db.ForeignKey('file_types.filetypeid'), nullable=False)
    templateid = db.Column(db.Integer, db.ForeignKey('output_templates.templateid'), nullable=False)
    date_generated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    search = db.relationship('Search', backref='outputs', lazy=True)
    file_type = db.relationship('FileType', backref='outputs', lazy=True)
    template = db.relationship('OutputTemplate', backref='outputs', lazy=True)

    def __repr__(self):
        return f'<Output {self.outputid}>'
