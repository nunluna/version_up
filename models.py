from database import db

class Software(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    current_version = db.Column(db.String(20), nullable=False)
    latest_version = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"Software({self.name}, {self.current_version}, {self.latest_version})"

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ip_address = db.Column(db.String(15), nullable=True)
    mac_address = db.Column(db.String(17), nullable=True)
    responsible_person = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Device({self.name}, {self.responsible_person})"

class InstalledSoftware(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    software_id = db.Column(db.Integer, db.ForeignKey('software.id'), nullable=False)
    installed_version = db.Column(db.String(20), nullable=False)

    device = db.relationship('Device', backref='installed_software')
    software = db.relationship('Software', backref='installed_software')

    def __repr__(self):
        return f"InstalledSoftware(Device {self.device_id}, Software {self.software_id}, {self.installed_version})"