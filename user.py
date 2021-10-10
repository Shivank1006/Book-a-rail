import functools
import psycopg2
import datetime
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/home')
def index():
    if g.user is None:
        return redirect(url_for('auth.login'))
    return render_template('user/index.html')


@bp.route('/schedule', methods=('GET', 'POST'))
def schedule():
    if g.user is None:
        return redirect(url_for('auth.login'))
    if session['admin'] is None:
        return redirect(url_for('user.index'))
    if request.method == 'POST':
        train_num = request.form['train_num']
        train_name = request.form['train_name']
        Source = request.form['Source']
        Destination = request.form['Destination']
        date = request.form['date']
        ac_coach = request.form['ac_coach']
        Sleeper_Coach = request.form['Sleeper_coach']
        

        conn = psycopg2.connect(database = "railways", user = "postgres", password = "xx", host = "127.0.0.1", port = "5432")
        cur = conn.cursor()

        error = None

        if not train_num:
            error = 'Train number is required.'
        elif not train_name:
            error = 'Train name is required.'
        elif not Source:
            error = 'Source is required.'
        elif not Destination:
            error = 'Destination is required.'
        elif not date:
            error = 'Date is required.'
        elif not ac_coach:
            error = 'Number of AC coaches are required.'
        elif not Sleeper_Coach:
            error = 'Number of sleeper coaches are required.'
        elif Source == Destination:
            error = 'Destination cannot be same as source.'
        elif int(Sleeper_Coach) > 12:
            error = 'Total number of sleeper coaches in a train should be less than 13.'
        elif int(ac_coach) > 12:
            error = 'Total number of AC coaches in a train should be less than 13.'
        elif int(Sleeper_Coach) + int(ac_coach) > 25 or int(Sleeper_Coach) + int(ac_coach) < 2:
            error = 'Total number of coaches in a train should be greater than 2 and less than 25.'
        else:
            cur.execute("""select * from trains where train_date='""" + date + """' and train_num='""" + train_num + """';""")
            if(cur.fetchone() is not None):
                error = 'Train is already scheduled for given ' + date + '.'

        if error is None:
            cur.execute("""INSERT INTO trains (train_num, train_name, source, destination, train_date, AC_num, sleeper_num) VALUES ('""" + train_num + """','""" + train_name + """','""" + Source + """','""" + Destination + """','""" + date + """','""" + ac_coach + """','""" + Sleeper_Coach + """');""")
            
            tdate = datetime.datetime.strptime(str(date), '%Y-%m-%d').strftime('%d_%m_%y')
            
            # creating a new table for each train
            train_id = str(train_num) + "_" + tdate
            cur.execute("""create table t""" + train_id + """ as (select coach, berth_no from ac_coach_no as a, ac_coach as ab where (val(a.coach)<= val('A""" + str(ac_coach) + """')) union select coach, berth_no from sleeper_coach_no as s, sleeper_coach as sb where (val(s.coach)<= val('S""" + str(Sleeper_Coach) + """')))""")
            cur.execute("""ALTER TABLE t""" + train_id + """ ADD COLUMN passenger INT, ADD COLUMN pnr BIGINT, ADD PRIMARY KEY (coach, berth_no);""")
            
            conn.commit()
            conn.close()
            return redirect('/home')

        flash(error)
        conn.commit()
        conn.close()
    return render_template('user/schedule.html')



@bp.route('/history')
def history():
    if g.user is None:
        return redirect(url_for('auth.login'))

    conn = psycopg2.connect(database = "railways", user = "postgres", password = "xx", host = "127.0.0.1", port = "5432")
    cur = conn.cursor()

    cur.execute("""select * from tickets where agent_username='""" + session['username'] +"""';""")
    history = cur.fetchall()
    info = []
    train_date = None
    res_class = None
    pnr = None
    for ticket in history:
        for i in range(ticket[1]):
            temp = []
            temp.append(ticket[3])
            cur.execute("""select * from trains where train_num='""" + str(ticket[3]) +"""';""")
            sdn = cur.fetchall()
            temp.append(sdn[0][1])
            temp.append(sdn[0][2])
            temp.append(sdn[0][3])

            temp.append(ticket[7])
            temp.append(ticket[8])
            temp.append(ticket[9])
            temp.append(ticket[10])
            temp.append(ticket[11])
            if ticket[5] == "AC":
                cur.execute("""select * from ac_coach where berth_no='""" + str(ticket[11]) +"""';""")
                sdn = cur.fetchall()
            else:
                cur.execute("""select * from sleeper_coach where berth_no='""" + str(ticket[11]) +"""';""")
                sdn = cur.fetchall()
            temp.append(sdn[0][1])
            
            
            if ticket[15] is not None:
                if ticket[5] == "AC":
                    cur.execute("""select * from ac_coach where berth_no='""" + str(ticket[16]) +"""';""")
                    sdn = cur.fetchall()
                else:
                    cur.execute("""select * from sleeper_coach where berth_no='""" + str(ticket[16]) +"""';""")
                    sdn = cur.fetchall()
                temp.append(sdn[0][1])
                temp.append(ticket[12])
                temp.append(ticket[13])
                temp.append(ticket[14])
                temp.append(ticket[15])
                temp.append(ticket[16])

            
            if ticket[20] is not None:
                if ticket[5] == "AC":
                    cur.execute("""select * from ac_coach where berth_no='""" + str(ticket[21]) +"""';""")
                    sdn = cur.fetchall()
                else:
                    cur.execute("""select * from sleeper_coach where berth_no='""" + str(ticket[21]) +"""';""")
                    sdn = cur.fetchall()
                temp.append(sdn[0][1])
                temp.append(ticket[17])
                temp.append(ticket[18])
                temp.append(ticket[19])
                temp.append(ticket[20])
                temp.append(ticket[21])

            
            if ticket[25] is not None:
                if ticket[5] == "AC":
                    cur.execute("""select * from ac_coach where berth_no='""" + str(ticket[26]) +"""';""")
                    sdn = cur.fetchall()
                else:
                    cur.execute("""select * from sleeper_coach where berth_no='""" + str(ticket[26]) +"""';""")
                    sdn = cur.fetchall()
                temp.append(sdn[0][1])
                temp.append(ticket[22])
                temp.append(ticket[23])
                temp.append(ticket[24])
                temp.append(ticket[25])
                temp.append(ticket[26])

        #train_date = ticket[4]
        #res_class = ticket[5]
        temp.append(ticket[4])
        temp.append(ticket[5])
        temp.append(ticket[0])
        temp.append(ticket[1])        

        info.append(temp)
    
    conn.commit()
    conn.close()
    return render_template('user/history.html', history = info, train_date=train_date, res_class = res_class, pnr = pnr)


@bp.route('/search', methods=('GET', 'POST'))
def search():
    if g.user is None:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        Source = request.form['Source']
        Destination = request.form['Destination']
        date = request.form['date']

        conn = psycopg2.connect(database = "railways", user = "postgres", password = "xx", host = "127.0.0.1", port = "5432")
        cur = conn.cursor()

        error = None

        if not Source:
            error = 'Source is required.'
        elif not Destination:
            error = 'Destination is required.'
        elif not date:
            error = 'Date is required.'
        elif Source == Destination:
            error = 'Destination cannot be same as source.'
        else:
            cur.execute("""select * from trains where source='""" + Source + """'and destination='""" + Destination + """' and train_date='""" + date + """';""")
        
            trains = cur.fetchall()
            info = []

            for train in trains:
                train = list(train)
                tdate = datetime.datetime.strptime(str(date), '%Y-%m-%d').strftime('%d_%m_%y')

                train_id = str(train[0]) + "_" + tdate
                
                cur.execute("""select count(*) from t""" + train_id + """ WHERE (pnr is null and coach LIKE 'A%');""")
                temp = cur.fetchall()
                train[5] = temp[0][0]

                cur.execute("""select count(*) from t""" + train_id + """ WHERE (pnr is null and coach LIKE 'S%');""")
                temp = cur.fetchall()
                train[6] = temp[0][0]

                info.append(train)



            conn.commit()
            conn.close()
            if len(trains) == 0:
                error = 'No train exists for given ' + Source + ' and ' + Destination + ' on ' + date + '.'

        if error is None:
            print(trains)
            return render_template('user/search.html', trains=info, Source=Source, dest=Destination)

        flash(error)
    return render_template('user/search.html')

@bp.route('/book', methods=('GET', 'POST'))
def book():
    if g.user is None:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        train_num = request.form['train_num']
        Source = request.form['Source']
        Destination = request.form['Destination']
        date = request.form['date']

        res_class = request.form['class']
        pass_num = request.form['pass_num']

        pass1 = request.form['pass1']
        gender1 = request.form['gender1']
        age1 = request.form['age1']

        pass2 = request.form['pass2']
        gender2 = request.form['gender2']
        age2 = request.form['age2']

        pass3 = request.form['pass3']
        gender3 = request.form['gender3']
        age3 = request.form['age3']

        pass4 = request.form['pass4']
        gender4 = request.form['gender4']
        age4 = request.form['age4']

        error = None

        if not train_num:
            error = 'Train number is required.'
        elif not Source:
            error = 'Source is required.'
        elif not Destination:
            error = 'Destination is required.'
        elif not date:
            error = 'Date is required.'
        elif not pass_num:
            error = 'Passenger number is required.'
        elif not res_class:
            error = 'Reservation class is required.'
        elif Source == Destination:
            error = 'Destination cannot be same as source.'
        else :

            tdate = datetime.datetime.strptime(str(date), '%Y-%m-%d').strftime('%d_%m_%y')
            train_id = str(train_num) + "_" + tdate

            conn = psycopg2.connect(database = "railways", user = "postgres", password = "xx", host = "127.0.0.1", port = "5432")
            cur = conn.cursor()

            # check if train exists for number, date, source, destination or not
            cur.execute("""select * from trains where source='""" + Source + """'and destination='""" + Destination + """' and train_date='""" + date + """' and train_num='""" + train_num + """';""")
            avai = cur.fetchall()
            if len(avai) == 0:
                error = 'Train not available.'


            if error is None and res_class == 'AC':
                cur.execute("""select count(*) from t""" + train_id + """ WHERE (pnr is null and coach LIKE 'A%');""")
                temp = cur.fetchall()
                if int(pass_num) > temp[0][0]:
                    error = 'Seats are not available.'

            if error is None and res_class == 'Sleeper':
                cur.execute("""select count(*) from t""" + train_id + """ WHERE (pnr is null and coach LIKE 'S%');""")
                temp = cur.fetchall()
                if int(pass_num) > temp[0][0]:
                    error = 'Seats are not available.'

        if error is None:
            # conn = psycopg2.connect(database = "railways", user = "postgres", password = "xx", host = "127.0.0.1", port = "5432")
            # cur = conn.cursor()
            
            # Make a entry in the tickets table with all details
            if int(pass_num) == 1 :
                cur.execute("""insert into tickets( num, agent_username, train_no,train_date, passenger1, age1, gender1, coach_type, booking_time) values (1,'""" + session['username'] + """', """ + train_num + """,'""" + date + """', '""" + pass1 + """', """ + age1 + """, '""" + gender1 + """','""" + res_class + """',now());""")
            elif int(pass_num) == 2 :
                cur.execute("""insert into tickets( num, agent_username, train_no,train_date, passenger1, age1, gender1, passenger2, age2, gender2, coach_type, booking_time) values (2,'""" + session['username'] + """', """ + train_num + """,'""" + date + """', '""" + pass1 + """', """ + age1 + """, '""" + gender1 + """', '""" + pass2 + """', """ + age2 + """, '""" + gender2 + """','""" + res_class + """',now());""")
            elif int(pass_num) == 3 :
                cur.execute("""insert into tickets( num, agent_username, train_no,train_date, passenger1, age1, gender1, passenger2, age2, gender2, passenger3, age3, gender3, coach_type, booking_time) values (3,'""" + session['username'] + """', """ + train_num + """,'""" + date + """', '""" + pass1 + """', """ + age1 + """, '""" + gender1 + """', '""" + pass2 + """', """ + age2 + """, '""" + gender2 + """', '""" + pass3 + """', """ + age3 + """, '""" + gender3 + """', '""" + res_class + """',now());""")
            elif int(pass_num) == 4 :
                cur.execute("""insert into tickets( num, agent_username, train_no,train_date, passenger1, age1, gender1, passenger2, age2, gender2, passenger3, age3, gender3,passenger4, age4, gender4, coach_type, booking_time) values (4,'""" + session['username'] + """', """ + train_num + """,'""" + date + """', '""" + pass1 + """', """ + age1 + """, '""" + gender1 + """', '""" + pass2 + """', """ + age2 + """, '""" + gender2 + """', '""" + pass3 + """', """ + age3 + """, '""" + gender3 + """', '""" + pass4 + """', """ + age4 + """, '""" + gender4 + """', '""" + res_class + """',now());""")
            
            conn.commit()
            conn.close()
            return redirect('/home')

        flash(error)
    return render_template('user/book.html')