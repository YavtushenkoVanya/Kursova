from flask import Flask, render_template, request, redirect, flash
import csv
import uuid

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Зчитуємо контакти з файлу CSV при запуску програми
def load_contacts_from_csv():
    contacts = []
    try:
        with open('contacts.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                contacts.append(row)
    except FileNotFoundError:
        pass
    return contacts

# Збереження контактів у файлі CSV
def save_contacts_to_csv(contacts):
    with open('contacts.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'name', 'address', 'email', 'phone']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for contact in contacts:
            writer.writerow(contact)

# Генерація унікального ідентифікатора для кожного контакту
def generate_contact_id():
    return str(uuid.uuid4())

# Завантаження контактів при запуску
contacts = load_contacts_from_csv()

@app.route('/')
def index():
    return render_template('index.html', contacts=contacts)

@app.route('/add_contact', methods=['GET', 'POST'])
def add_contact():
    if request.method == 'POST':
        contact_id = generate_contact_id()
        name = request.form['name']
        address = request.form['address']
        email = request.form['email']
        phone = request.form['phone']
        contacts.append({'id': contact_id, 'name': name, 'address': address, 'email': email, 'phone': phone})
        save_contacts_to_csv(contacts)
        flash("Контакт успішно додано", "success")
        return redirect('/')
    return render_template('add_contact.html')

@app.route('/edit_contact/<contact_id>', methods=['GET', 'POST'])
def edit_contact(contact_id):
    contact = next((c for c in contacts if c['id'] == contact_id), None)
    if not contact:
        flash("Контакт не знайдено", "error")
        return redirect('/')

    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        email = request.form['email']
        phone = request.form['phone']

        contact['name'] = name
        contact['address'] = address
        contact['email'] = email
        contact['phone'] = phone

        save_contacts_to_csv(contacts)
        flash("Контакт успішно оновлено", "success")
        return redirect('/')

    return render_template('edit_contact.html', contact=contact)

@app.route('/delete_contact/<contact_id>', methods=['GET', 'POST'])
def delete_contact(contact_id):
    contact = next((c for c in contacts if c['id'] == contact_id), None)
    if not contact:
        flash("Контакт не знайдено", "error")
        return redirect('/')

    if request.method == 'POST':
        contacts.remove(contact)
        save_contacts_to_csv(contacts)
        flash("Контакт успішно видалено", "success")
        return redirect('/')

    return render_template('delete_contact.html', contact=contact)

@app.route('/search_results', methods=['GET', 'POST'])
def search_results():
    if request.method == 'POST':
        search_query = request.form['search_query']
        results = []
        for contact in contacts:
            if search_query.lower() in contact['name'].lower() or search_query in contact['phone']:
                results.append(contact)
        return render_template('search_results.html', results=results, query=search_query)
    return render_template('search.html')

if __name__ == '__main__':
    app.run(port=8080)
