from flask import Flask, render_template, request, redirect, url_for

#Init app
app = Flask(__name__)

# URI, endpoint

db =[]
@app.route ('/', methods =['GET', 'POST'])
def main():
    if request.method == 'POST':
        new_task = request.form['new_task']
        if len(new_task) > 0 and new_task not in db:
            db.append(new_task)

    # else: 
    #     tasks = 

    # context = {
    #     todo : 'sssng'
    # }

    return render_template('index.html', todo = db, name = 'Sssng')


@app.route('/delete/<task>', methods=['GET','POST'])
def delete(task):
    db.remove(task)
    return redirect(url_for('main'))




@app.route('/update/<task>', methods=['GET','POST'])
def update(task , update_task):
    for key, value in enumerate(db):
        if key == task:
            db[key]= update_task
        return redirect(url_for('details.html', todo = db, name = 'Sssng'))
    
    return redirect(url_for('main'))



if __name__ == '__main__':
    #Only in development
    app.run(debug=True)