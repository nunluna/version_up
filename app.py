from flask import Flask, render_template, request, redirect, url_for
from database import db
from version_fetcher import fetch_latest_version  # Импорт модуля

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///version_control.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

from models import Software, Device, InstalledSoftware


# Функция сравнения версий
def is_version_outdated(installed_version, latest_version):
    try:
        installed_parts = [int(x) for x in installed_version.split('.')]
        latest_parts = [int(x) for x in latest_version.split('.')]
        return installed_parts < latest_parts
    except (ValueError, AttributeError):
        return installed_version != latest_version


# Инициализация базы данных
with app.app_context():
    db.create_all()

# Главная страница
@app.route('/')
def index():
    software_list = Software.query.all()
    devices = Device.query.all()
    installed = InstalledSoftware.query.all()

    # Обновляем актуальные версии с помощью модуля
    for software in software_list:
        latest_version = fetch_latest_version(software.name)
        if latest_version != "Неизвестно":
            software.latest_version = latest_version
    db.session.commit()

    # Проверяем статус актуальности
    for inst in installed:
        inst.outdated = is_version_outdated(inst.installed_version, inst.software.latest_version)

    # Список предустановленных ПО
    predefined_software = [
        {'name': 'Visual Studio Code'},
        {'name': 'PyCharm'},
        {'name': 'Git'},
        {'name': 'Node.js'},
        {'name': 'Python'},
        {'name': 'Docker'},
        {'name': 'Kubernetes'},
        {'name': 'IntelliJ IDEA'},
        {'name': 'WebStorm'},
        {'name': 'Ruby'},
        {'name': 'Rails'},
        {'name': 'PHP'},
        {'name': 'Laravel'},
        {'name': 'Java'},
        {'name': 'Android Studio'}
    ]

    # Для каждого ПО добавляем актуальную версию
    for software in predefined_software:
        software['latest_version'] = fetch_latest_version(software['name'])

    return render_template('index.html', software_list=software_list, devices=devices, installed=installed, predefined_software=predefined_software)

# Маршрут для списка ПО
@app.route('/software_list')
def software_list():
    software_list = Software.query.all()  # Получаем все ПО из базы данных
    predefined_software = [
        {'name': 'Visual Studio Code', 'latest_version': fetch_latest_version('Visual Studio Code')},
        {'name': 'PyCharm', 'latest_version': fetch_latest_version('PyCharm')},
        {'name': 'Git', 'latest_version': fetch_latest_version('Git')},
        {'name': 'Node.js', 'latest_version': fetch_latest_version('Node.js')},
        {'name': 'Python', 'latest_version': fetch_latest_version('Python')},
        {'name': 'Docker', 'latest_version': fetch_latest_version('Docker')},
        {'name': 'Kubernetes', 'latest_version': fetch_latest_version('Kubernetes')},
        {'name': 'IntelliJ IDEA', 'latest_version': fetch_latest_version('IntelliJ IDEA')},
        {'name': 'WebStorm', 'latest_version': fetch_latest_version('WebStorm')},
        {'name': 'Ruby', 'latest_version': fetch_latest_version('Ruby')},
        {'name': 'Rails', 'latest_version': fetch_latest_version('Rails')},
        {'name': 'PHP', 'latest_version': fetch_latest_version('PHP')},
        {'name': 'Laravel', 'latest_version': fetch_latest_version('Laravel')},
        {'name': 'Java', 'latest_version': fetch_latest_version('Java')},
        {'name': 'Android Studio', 'latest_version': fetch_latest_version('Android Studio')}
    ]
    return render_template('software_list.html', software_list=software_list, predefined_software=predefined_software)

# Страница для добавления нового ПО
@app.route('/add_software', methods=['GET', 'POST'])
def add_software():
    if request.method == 'POST':
        name = request.form['name']
        current_version = request.form['current_version']
        latest_version = fetch_latest_version(name)
        if latest_version == "Unknown":
            latest_version = request.form['latest_version']
        software = Software(name=name, current_version=current_version, latest_version=latest_version)
        db.session.add(software)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_software.html')

# Страница для редактирования ПО
@app.route('/edit_software/<int:id>', methods=['GET', 'POST'])
def edit_software(id):
    software = Software.query.get_or_404(id)
    if request.method == 'POST':
        software.name = request.form['name']
        software.current_version = request.form['current_version']
        latest_version = fetch_latest_version(software.name)
        if latest_version == "Unknown":
            latest_version = request.form['latest_version']
        software.latest_version = latest_version
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_software.html', software=software)

# Страница для удаления ПО
@app.route('/delete_software/<int:id>', methods=['POST'])
def delete_software(id):
    software = Software.query.get_or_404(id)
    db.session.delete(software)
    db.session.commit()
    return redirect(url_for('index'))

# Страница для добавления устройства
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

# Страница для редактирования устройства
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

# Страница для удаления устройства
@app.route('/delete_device/<int:id>', methods=['POST'])
def delete_device(id):
    device = Device.query.get_or_404(id)
    db.session.delete(device)
    db.session.commit()
    return redirect(url_for('index'))

# Страница для добавления установленного ПО
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

# Страница для редактирования установленного ПО
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

# Страница для удаления установленного ПО
@app.route('/delete_installed_software/<int:id>', methods=['POST'])
def delete_installed_software(id):
    installed = InstalledSoftware.query.get_or_404(id)
    db.session.delete(installed)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
