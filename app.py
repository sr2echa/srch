import flask
from flask import request,Flask,redirect,render_template

import sqlite3
import os
from threading import Thread

app = flask.Flask(__name__, template_folder='.')
app.config["DEBUG"] = False


def run():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

def redbull():
    t = Thread(target=run)
    t.start()  


@app.route('/api/', methods=['GET'])
def home():
    #get the data stored in db.sqlite as a dictionary from table default srch
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("SELECT * FROM srch")
    search = dict(c.fetchall())
    conn.close()
    #get the data stored in db.sqlite3 as a dictionary from table default
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('SELECT * FROM engine')
    default_engine = dict(c.fetchall())
    conn.close()

    

    #return (flask.render_template('home.html', srch=srch, default=default))
    

    '''
    fallback = request.args['default']
    if fallback:
        return redirect(fallback)
    else:
        return redirect('https://www.google.com/')
    '''
    #Prefix
    if "prefix" in request.args:
        prefix=request.args.get('prefix')
    else:
        prefix="!"
    ###

    #Default_Engine
    if "default" in request.args:
        default=request.args.get('default')
        if default in default_engine:
            default=default_engine[default]
    else:
        default="https://www.google.com/search?q="
    ###

    #Search_Engine
    if "s" in request.args:
        s=request.args.get('s')

        # localhost
        if s[:3]=="lh:":
            q=s.split(sep=":")[-1]
            #return f"<h1>{q}</h1>"
            return redirect(f'localhost:{q}')
        elif s=="lh":
            return redirect(f'https://localhost:3000')
        ###

        #reddit
        if s[:2]=="r/":
            q=s.partition("/")[-1]
            return redirect(f'https://www.reddit.com/r/{q}')
        elif s[:2]=="u/":
            q=s.partition("/")[-1]
            return redirect(f'https://www.reddit.com/u/{q}')
        ###

        if s[0]==prefix:
            s,s_ = s[1:],s
            s=s.partition(' ')
            #print(s)
            #print(search[s[0]])
            if s[0] in search:
                #if s[-1]=="" return search[s[0]] untill occurence of 3 /
                if s[-1]=="":
                    count,q=0,""
                    for i in search[s[0]][2:]:
                        q+=i
                        if i=="/":
                            count+=1
                        if count==3:
                            return redirect(q)
                #replace " " with "+" in search term
                q=s[-1].replace(" ","+")
                return redirect(eval(search[s[0]]))
            else:
              return redirect (default+s_)
        else:
            q=s.replace(" ","+")
            return redirect(default+q)
    
    '''
    if "default" in request.args:
        fallback=request.args["default"]
        if fallback=="":
            fallback="https://www.google.com"
            return redirect(fallback)
    '''
    
    #check if prefix == 1st letter of ar

    '''
    if 's' in request.args:
        srch=request.args.get('s')
        if srch[0]==prefix:
            srch=srch.split()
            #if srch[0]=="!amazon":
            #return f"<h1>{srch}</h1>"
            q=""
            for i in srch[1:]:
                q+=i
            if srch[0] in search:
                return redirect(search[srch[0][1:]]+q)
        else:
            return "<h1>No search engine found</h1>"
    '''

    #return "<h1>SRCH</h1><p>Supercharge your web searches</p>"
    return redirect('../')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


if __name__ == "__main__":
    redbull()
    #app.run()
