from flask import Flask, render_template, request, redirect, url_for
from database import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///version_control.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

from models import Software, Device, InstalledSoftware


def is_version_outdated(installed_version, latest_version):
    try:
        installed_parts = [int(x) for x in installed_version.split('.')]
        latest_parts = [int(x) for x in latest_version.split('.')]
        return installed_parts < latest_parts
    except (ValueError, AttributeError):
        # Если версии не в формате X.Y.Z, считаем их разными
        return installed_version != latest_version


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    software_list = Software.query.all()
    devices = Device.query.all()
    installed = InstalledSoftware.query.all()

    # Добавляем статус актуальности для каждой записи
    for inst in installed:
        inst.outdated = is_version_outdated(inst.installed_version, inst.software.latest_version)

    return render_template('index.html', software_list=software_list, devices=devices, installed=installed)


@app.route('/add_software', methods=['GET', 'POST'])
def add_software():
    if request.method == 'POST':
        name = request.form['name']
        current_version = request.form['current_version']
        latest_version = request.form['latest_version']
        software = Software(name=name, current_version=current_version, latest_version=latest_version)
        db.session.add(software)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_software.html')


@app.route('/edit_software/<int:id>', methods=['GET', 'POST'])
def edit_software(id):
    software = Software.query.get_or_404(id)
    if request.method == 'POST':
        software.name = request.form['name']
        software.current_version = request.form['current_version']
        software.latest_version = request.form['latest_version']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_software.html', software=software)


@app.route('/delete_software/<int:id>', methods=['POST'])
def delete_software(id):
    software = Software.query.get_or_404(id)
    db.session.delete(software)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/add_device', methods=['GET', 'POST'])
def add_device():
    if request.method == 'POST':
        name = request.form['name']
        ip_address = request.form['ip_address']
        mac_address = request.form['mac_address']
        responsible_person = request.form['responsible_person']
        device = Device(
            name=name,
            ip_address=ip_address if ip_address else None,
            mac_address=mac_address if mac_address else None,
            responsible_person=responsible_person
        )
        db.session.add(device)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_device.html')


@app.route('/edit_device/<int:id>', methods=['GET', 'POST'])
def edit_device(id):
    device = Device.query.get_or_404(id)
    if request.method == 'POST':
        device.name = request.form['name']
        device.ip_address = request.form['ip_address'] if request.form['ip_address'] else None
        device.mac_address = request.form['mac_address'] if request.form['mac_address'] else None
        device.responsible_person = request.form['responsible_person']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_device.html', device=device)


@app.route('/delete_device/<int:id>', methods=['POST'])
def delete_device(id):
    device = Device.query.get_or_404(id)
    db.session.delete(device)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/add_installed_software', methods=['GET', 'POST'])
def add_installed_software():
    if request.method == 'POST':
        device_id = request.form['device_id']
        software_id = request.form['software_id']
        installed_version = request.form['installed_version']
        installed_software = InstalledSoftware(
            device_id=device_id,
            software_id=software_id,
            installed_version=installed_version
        )
        db.session.add(installed_software)
        db.session.commit()
        return redirect(url_for('index'))
    devices = Device.query.all()
    softwares = Software.query.all()
    return render_template('add_installed_software.html', devices=devices, softwares=softwares)


@app.route('/edit_installed_software/<int:id>', methods=['GET', 'POST'])
def edit_installed_software(id):
    installed = InstalledSoftware.query.get_or_404(id)
    if request.method == 'POST':
        installed.device_id = request.form['device_id']
        installed.software_id = request.form['software_id']
        installed.installed_version = request.form['installed_version']
        db.session.commit()
        return redirect(url_for('index'))
    devices = Device.query.all()
    softwares = Software.query.all()
    return render_template('edit_installed_software.html', installed=installed, devices=devices, softwares=softwares)


@app.route('/delete_installed_software/<int:id>', methods=['POST'])
def delete_installed_software(id):
    installed = InstalledSoftware.query.get_or_404(id)
    db.session.delete(installed)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)