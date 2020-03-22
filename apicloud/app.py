from flask import Flask, render_template, url_for, flash, redirect

from forms import SearchNoteForm, AddNote
from flask import flash, render_template, request, redirect
from datetime import datetime
import pymongo
from pymongo import MongoClient
import json

client = MongoClient("mongodb://myUserAdmin:abc123@ec2-3-87-16-135.compute-1.amazonaws.com:27017")
db = client.mydb
mydb = client["mydb"]
mycol = db["books"]

#myclient = pymongo.MongoClient("mongodb://localhost:27017/")
#mydb = myclient["gutenberg"]
#mycol = mydb["books"]
 
testing  = False

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aaa'


def add_note(search1, note1):
    notedict = { "Keyword": search1, "Note": note1}
    with open('file.json', 'a') as f:
        json.dump(notedict, f, separators=(',', ':'))
        f.write('\n')
    f.close

def add_catalogue(search1, mydoc):
    with open('catalogue.json', 'a') as cat:
     for res in mydoc:
        catalogue = { "Author": search1, "Title": res['Title'] }
        json.dump(catalogue, cat, separators=(',', ':'))
        cat.write('\n')
    cat.close


@app.route('/', methods=['GET', 'POST'])
def index():
    c = open('counter.txt', 'w') 
    c.write('0')
    c.close
    freqcount = 0
    search = SearchNoteForm(request.form)
    if request.method == 'POST':
            if 'submit1' in request.form:
                date = request.form.get('search')
                time = datetime.now()
                return redirect(url_for('search_results', search=date, time = time, freqcount = freqcount))
            if 'submit2' in request.form:
                return redirect('/notes')
                #flash(msg)         
    

    return render_template('index.html', form=search)



@app.route('/results', methods=['GET', 'POST'])


def search_results():
    results = []  
    search = request.args.get('search', None)
    time = request.args.get('time',None)
    c = open('counter.txt', 'r') 
    freqcount = c.readline()
    c.close()
    
    myquery = { "Author": search }
    test = mycol.find_one(myquery)
    mydoc=mycol.find(myquery)
    catalog = mycol.find(myquery)
    form2 = AddNote(request.form)
    notedict, retdict = {}, {}
    ret = []
    errmsg = "Invalid Keyword!!!"
    flag = 1
    mydoc.rewind()

    if 'submit2' in request.form:
                flash("Note Saved")
                note = request.form.get('addnote')
                if (note == ""):
                    flash("Please enter a valid note!!")
                if test:
                    add_note(search,note)
    

    if 'ret' in request.form:
                flash("Note Retrieved")
                keyword = request.form.get('retnote')
                if(keyword== ""):
                    flash("Please enter a valid keyword!!")

                if test:
                    with open('file.json') as f:
                      for line in f:
                        ret.append(json.loads(line))
                      return render_template('results.html', mydoc='', results = ret, val = keyword, error=errmsg, form=form2)
                
                if 'cancel2' in request.form:
                     return render_template('results.html', mydoc=mydoc, results = results, form=form2, flag = flag)
   

    if 'cancel' in request.form:
        return redirect('/')          


    if search == '':
        results = "Nothing entered"
        return render_template('results.html', results=results, mydoc = '')

    if search != '':
        flag = 0
        file1 = open("Search Log.txt","a") 
        freqcount = int(freqcount) + 1
        c = open('counter.txt', 'w') 
        c.write(str(freqcount))
        c.close
        z = "Keyword : %s\nTime : %s\nFrequency count : %s" % (search,time,freqcount)
        file1.write(z)
        file1.write("\n")
        if test:
            
            add_catalogue(search,catalog)
            return render_template('results.html', mydoc=mydoc, results = results, form=form2, flag = flag)

        else :
            flash("No Query results found, re-enter")

    if not results:
        flash('No results found!')
        return redirect('/')
    else:

        # display results
        return render_template('results.html', results=results)




if __name__ == '__main__':
    app.run(debug=True)
