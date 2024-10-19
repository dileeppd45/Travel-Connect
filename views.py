from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
import datetime


# Create your views here.

def login_home(request):
    return render(request,'login_home.html')

def login(request):
    if request.method == 'POST':
        idname = request.POST['name']
        password = request.POST['password']
        cursor = connection.cursor()
        cursor.execute("select * from login where admin_id = '"+str(idname)+"' and password = '"+str(password)+"'")
        admin = cursor.fetchone()
        if admin == None:
            cursor = connection.cursor()
            cursor.execute("select * from user_register where phone = '" + str(idname) + "' and password = '" + str(password) + "'")
            data = cursor.fetchone()
            if data == None:
                cursor = connection.cursor()
                cursor.execute("select * from user_register where email = '" + str(idname) + "' and password = '" + str(password) + "'")
                data = cursor.fetchone()
                if data == None:
                    return HttpResponse("<script>alert('incorrect datas please validate ');window.location='../loginhome';</script>")
                else:
                    request.session["uid"]= data[0]
                    return HttpResponse("<script>alert('welcome "+data[1]+" ');window.location='../userhome';</script>")
            else:
                request.session["uid"] = data[0]
                return HttpResponse("<script>alert('welcome " + data[1] + " ');window.location='../userhome';</script>")
        else:
            request.session["adminid"] = idname
            return redirect(admin_home)
    else:
        return render(request,'login.html')

def signin(request):
    if request.method == 'POST':
        name = request.POST['name']
        address = request.POST['address']
        phone = request.POST['phone']
        email = request.POST['email']
        password = request.POST['password']
        cursor = connection.cursor()
        cursor.execute("select * from user_register where phone='"+phone+"' or email = '"+str(email)+"'")
        data = cursor.fetchone()
        if data ==None:
            cursor.execute("insert into user_register values(null,'"+name+"','"+address+"','"+phone+"','"+email+"','"+password+"')")
            request.session['uid'] = cursor.lastrowid
            return HttpResponse("<script>alert('welcome " +name+ " ');window.location='../userhome';</script>")
        else:
            return HttpResponse("<script>alert('email or phone number already registered please add your email and password as unique');window.location='../loginhome';</script>")








def admin_home(request):
    cursor = connection.cursor()
    cursor.execute("select * from plan where status ='active' or status='running'")
    aata = cursor.fetchall()
    for i in aata:
        plan_time =i[6]
        cursor.execute("select * from route where route_type='end point' and idplan ='"+str(i[0])+"' ")
        enddata=cursor.fetchone()
        end_time = enddata[7]

        import datetime
        plan_time = datetime.datetime.strptime(plan_time, '%Y-%m-%d %H:%M:%S')
        end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
        # plan_time_minus_1_hour = plan_time - datetime.timedelta(hours=1)
        # print(plan_time_minus_1_hour)
        current_datetime = datetime.datetime.now()
        if end_time >= current_datetime >= plan_time:
            cursor.execute("update plan set status ='running' where idplan='"+str(i[0])+"' ")
        if end_time < current_datetime:
            cursor.execute("update plan set status ='completed' where idplan='"+str(i[0])+"' ")

            # return HttpResponse("<script>alert('sorry you cant update. there is only less than 1 hour left. so be ready to start  plan on "+str(plan_time)+"');window.location='../view_my_veh';</script>")



    return render(request,'admin/index1.html')

def districts(request):
    cursor = connection.cursor()
    cursor.execute("select * from district ")
    data = cursor.fetchall()
    return render(request,'admin/district.html',{'data':data})

def add_town(request,id):
    cursor = connection.cursor()
    cursor.execute("select * from district where district_id ='"+id+"'")
    mata = cursor.fetchone()
    request.session['distid'] = id
    if request.method == 'POST':
        town = request.POST['town']
        details=request.POST['details']
        cursor.execute("select * from town where name ='"+town+"' and district_id ='"+id+"' ")
        data = cursor.fetchone()
        if data == None:
            cursor.execute("insert into town values(null,'"+town+"','"+id+"','"+details+"')")
            return redirect('add_town',id=id)
        else:
            return HttpResponse("<script>alert('town  named " + town + " already exist in  district "+mata[1]+" ');window.location='../districts';</script>")

    return render(request,'admin/add_town.html',{'district':mata[1]})

def view_town(request,id):
    cursor = connection.cursor()
    cursor.execute("select * from district where district_id ='"+id+"' ")
    mata = cursor.fetchone()
    cursor.execute("select * from town where district_id ='"+id+"' ")
    data = cursor.fetchall()
    return render(request,'admin/town.html',{'district':mata[1],'data':data})

# def veh_approved(request):
#     cursor = connection.cursor()
#     cursor.execute("select * from vehicle_register where status ='approved' ")
#     data = cursor.fetchall()
#     return render(request,'veh_approved.html',{'data':data})

def veh_pending(request):
    cursor = connection.cursor()
    cursor.execute("select * from vehicle_register join user_register where status ='pending' and vehicle_register.user_id = user_register.user_id ")
    data = cursor.fetchall()
    return render(request,'admin/veh_pending.html',{'data':data})
def approve_veh(request,id):
    cursor = connection.cursor()
    cursor.execute("update vehicle_register set status ='approved' where vehicle_number ='"+id+"'")
    return redirect(veh_pending)

def reject_veh(request,id):
    cursor = connection.cursor()
    cursor.execute("update vehicle_register set status ='rejected' where vehicle_number ='"+id+"'")
    return redirect(veh_pending)

def admin_view_plan(request):
    cursor = connection.cursor()
    cursor.execute("select * from plan where status ='active' or status='running'")
    aata = cursor.fetchall()
    for i in aata:
        plan_time =i[6]
        cursor.execute("select * from route where route_type='end point' and idplan ='"+str(i[0])+"' ")
        enddata=cursor.fetchone()
        end_time = enddata[7]

        import datetime
        plan_time = datetime.datetime.strptime(plan_time, '%Y-%m-%d %H:%M:%S')
        end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
        # plan_time_minus_1_hour = plan_time - datetime.timedelta(hours=1)
        # print(plan_time_minus_1_hour)
        current_datetime = datetime.datetime.now()
        if end_time >= current_datetime >= plan_time:
            cursor.execute("update plan set status ='running' where idplan='"+str(i[0])+"' ")
        if end_time < current_datetime:
            cursor.execute("update plan set status ='completed' where idplan='"+str(i[0])+"' ")
    cursor.execute("select plan.*,a.name,b.name,u.name,u.phone,u.email,v.* from plan join town as a join town as b join user_register as u join vehicle_register as v where plan.user_id = u.user_id and plan.vehid = v.vehicle_number and u.user_id = v.user_id and plan.status ='active' and plan.start =a.town_id and plan.end =b.town_id")
    plansa = cursor.fetchall()
    cursor.execute("select plan.*,a.name,b.name,u.name,u.phone,u.email,v.* from plan join town as a join town as b join user_register as u join vehicle_register as v where plan.user_id = u.user_id and plan.vehid = v.vehicle_number and u.user_id = v.user_id and plan.status ='running' and plan.start =a.town_id and plan.end =b.town_id")
    plansr = cursor.fetchall()
    cursor.execute("select plan.*,a.name,b.name,u.name,u.phone,u.email,v.* from plan join town as a join town as b join user_register as u join vehicle_register as v where plan.user_id = u.user_id and plan.vehid = v.vehicle_number and u.user_id = v.user_id and  plan.status ='completed' and plan.start =a.town_id and plan.end =b.town_id")
    plansc = cursor.fetchall()
    return render(request,'admin/view_planv.html',{'active':plansa,'running':plansr,'completed':plansc})

def view_aroutec(request,id):
    cursor = connection.cursor()
    cursor.execute("select plan.*,a.name,b.name from plan join town as a join town as b where  plan.idplan='"+id+"' and plan.start =a.town_id and plan.end =b.town_id")
    plansa = cursor.fetchone()
    print(plansa)
    cursor.execute("select * from vehicle_register where vehicle_number='"+plansa[2]+"' ")
    veh = cursor.fetchone()
    print(veh)
    cursor.execute("select * from route where idplan ='"+str(id)+"' and status ='active'")
    data = cursor.fetchall()
    routcount =len(data)
    print(routcount)
    s=[]
    for i in range(1,routcount):
        print(i)
        
        cursor.execute("select route.*,town.town_id,town.name from route join town  where route.route_num ='"+str(i)+"' and route.town = town.town_id and route.idplan='"+id+"'")
        a = cursor.fetchone()
        cursor.execute("select route.*,town.town_id,town.name from route join town where route.route_num ='"+str(i+1)+"' and route.town = town.town_id and route.idplan='"+id+"' ")
        b = cursor.fetchone()
        print(a)
        print(b)
        sa =(str(a[4]),str(b[4]),str(a[0]),str(b[0]),str(a[9]),str(b[9]),str(a[7]),str(b[7]))
        s.append(sa)
    s=tuple(s)
    print(s)
    request.session['viewed_planid']=str(a[1])
    return render(request,'admin/view_routec.html',{'s':s,'vehicle':veh,'active':plansa})
    
def view_adbookings(request,id):
    cursor = connection.cursor()
    cursor.execute("select plan.*,a.name,b.name from plan join town as a join town as b where  plan.idplan='"+id+"' and plan.start =a.town_id and plan.end =b.town_id")
    plansa = cursor.fetchone()
    print(plansa)
    cursor.execute("select * from plan where idplan='"+id+"'")
    data = cursor.fetchone()
    vehno=data[2]
    cursor.execute("select * from vehicle_register where vehicle_number='"+vehno+"' ")
    veh = cursor.fetchone()
    print(veh)
    cursor.execute("select * from travel_booking where idplan = '"+id+"' ")
    data = cursor.fetchone()
    if data==None:
            return HttpResponse("<script>alert('No Bookings'); window.location='../admin_view_plan';</script>")
    cursor.execute("select u.name,u.phone,u.email,dia.name,ta.name,t.stime,dib.name,tb.name,t.etime,t.seats,t.booked_time from travel_booking as t join route as ra join route as rb join town as ta join town as tb join district as dia join district as dib join user_register as u where t.idplan = '"+id+"' and t.start = ra.idroute and t.end = rb.idroute and ra.town = ta.town_id and rb.town = tb.town_id and ta.district_id = dia.district_id and tb.district_id = dib.district_id and t.user_id = u.user_id ")
    data =cursor.fetchall()
    print(data,"data")
    return render(request,'admin/view_dbookings.html',{'data':data,'vehicle':veh,'active':plansa})



def admin_logout(request):
    return render(request,'admin/LogOut.html')




def user_home(request):
    print(request.session['uid'])
    cursor = connection.cursor()
    cursor.execute("select * from plan where status ='active' or status = 'running'")
    aata = cursor.fetchall()
    for i in aata:
        plan_time =i[6]
        cursor.execute("select * from route where route_type='end point' and idplan ='"+str(i[0])+"' ")
        enddata=cursor.fetchone()
        end_time = enddata[7]

        import datetime
        plan_time = datetime.datetime.strptime(plan_time, '%Y-%m-%d %H:%M:%S')
        end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
        # plan_time_minus_1_hour = plan_time - datetime.timedelta(hours=1)
        # print(plan_time_minus_1_hour)
        current_datetime = datetime.datetime.now()
        if end_time >= current_datetime >= plan_time:
            cursor.execute("update plan set status ='running' where idplan='"+str(i[0])+"' ")
        if end_time < current_datetime:
            cursor.execute("update plan set status ='completed' where idplan='"+str(i[0])+"' ")
    return render(request,'user/index1.html')

def reg_my_veh(request):
    uid = request.session['uid']
    cursor = connection.cursor()
    cursor.execute("select * from user_register where user_id ='"+str(uid)+"'")
    mata = cursor.fetchone()
    if request.method == 'POST':
        veh_no = request.POST['veh_no']
        manufacturer = request.POST['anufacturer']
        model = request.POST['model']
        reg_year = request.POST['reg_year']
        cursor.execute("select * from vehicle_register where vehicle_number ='"+veh_no+"'")
        data = cursor.fetchone()
        if data==None:
            cursor.execute("insert into vehicle_register values('"+str(veh_no)+"','"+str(uid)+"','"+str(manufacturer)+"','"+str(model)+"','"+str(reg_year)+"','pending')")
            return redirect(user_home)
        else:
            return HttpResponse("<script>alert('vehicle you entered already in use ');window.location='../userhome';</script>")
    return render(request,'user/register_vehicle.html',{'name':mata[1]})

def view_my_veh(request):
    uid = request.session['uid']
    cursor = connection.cursor()
    cursor.execute("select * from plan where status ='active' or status = 'running'")
    aata = cursor.fetchall()
    for i in aata:
        plan_time =i[6]
        cursor.execute("select * from route where route_type='end point' and idplan ='"+str(i[0])+"' ")
        enddata=cursor.fetchone()
        end_time = enddata[7]

        import datetime
        plan_time = datetime.datetime.strptime(plan_time, '%Y-%m-%d %H:%M:%S')
        end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
        # plan_time_minus_1_hour = plan_time - datetime.timedelta(hours=1)
        # print(plan_time_minus_1_hour)
        current_datetime = datetime.datetime.now()
        if end_time >= current_datetime >= plan_time:
            cursor.execute("update plan set status ='running' where idplan='"+str(i[0])+"' ")
        if end_time < current_datetime:
            cursor.execute("update plan set status ='completed' where idplan='"+str(i[0])+"' ")
    cursor.execute("select * from vehicle_register where status ='approved' and user_id='"+str(uid)+"'")
    data = cursor.fetchall()
    cursor.execute("select * from vehicle_register where status ='pending' and user_id='"+str(uid)+"'")
    pdata = cursor.fetchall()
    return render(request,'user/view_my_veh.html',{'data':data,'pdata':pdata})




    # return render(request,'user_home.html')
def user_logout(request):
    return render(request,'user/LogOut.html')




def add_plan(request,id):
    cursor = connection.cursor()
    cursor.execute("select * from plan where status ='active' or status = 'running'")
    aata = cursor.fetchall()
    for i in aata:
        plan_time =i[6]
        cursor.execute("select * from route where route_type='end point' and idplan ='"+str(i[0])+"' ")
        enddata=cursor.fetchone()
        end_time = enddata[7]

        import datetime
        plan_time = datetime.datetime.strptime(plan_time, '%Y-%m-%d %H:%M:%S')
        end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
        # plan_time_minus_1_hour = plan_time - datetime.timedelta(hours=1)
        # print(plan_time_minus_1_hour)
        current_datetime = datetime.datetime.now()
        if end_time >= current_datetime >= plan_time:
            cursor.execute("update plan set status ='running' where idplan='"+str(i[0])+"' ")
        if end_time < current_datetime:
            cursor.execute("update plan set status ='completed' where idplan='"+str(i[0])+"' ")
    cursor.execute("select * from vehicle_register where vehicle_number ='"+str(id)+"'")
    data = cursor.fetchone()
    if request.method == 'POST':
        start = request.POST['town']
        end = request.POST['etown']
        date = request.POST['date']
        edate = request.POST['edate']
        seats=request.POST['seats']
        if start == end:
            return HttpResponse("<script>alert('you selected same town as start point and end point. Select different towns');window.location='../view_my_veh';</script>")
        # current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # # Perform JavaScript validation on the date
        # input_datetime = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M') 
        # # input_dates=input_datetime.date() # Assuming datetime-local format
        # if input_date <= datetime.datetime.now():
        #     return HttpResponse("<script>alert('Please select a date and time greater than 2 hours from now.');window.location='../view_my_veh';</script>")
        # print(start,end,date,seats,current_datetime,input_datetime)
        import datetime
        from datetime import timedelta
        current_datetime = datetime.datetime.now()
        print(current_datetime,'current_datetime')
        input_datetime = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M')
        input_edatetime = datetime.datetime.strptime(edate, '%Y-%m-%dT%H:%M')
        print(input_datetime,'input_date_time')

        cursor.execute("select * from plan where vehid ='"+str(id)+"' and  status ='active' or vehid ='"+str(id)+"' and status ='running'")
        ssata = cursor.fetchall()
        for i in ssata:
            cursor.execute("select * from route where route_type='end point' and idplan = '"+str(i[0])+"'")
            nancy = cursor.fetchone()
            existstime = i[6]
            existetime = nancy[7]
            existstime = datetime.datetime.strptime(existstime, '%Y-%m-%d %H:%M:%S')
            existetime = datetime.datetime.strptime(existetime, '%Y-%m-%d %H:%M:%S')
            if existstime <=input_datetime <= existetime:
                return HttpResponse("<script>alert('you already have a plan in this time .');window.location='../view_my_veh';</script>")
            if existstime <=input_edatetime <= existetime:
                return HttpResponse("<script>alert('you already have a plan in this time .');window.location='../view_my_veh';</script>")
        
        future_datetime = current_datetime + timedelta(hours=2)
        print(future_datetime,'future_datetime')
        if input_datetime <= future_datetime:
            return HttpResponse("<script>alert('Please select a date and time greater than 2 hours from now.');window.location='../view_my_veh';</script>")
        validetime =input_datetime + timedelta(hours=1)
        if input_edatetime <validetime:
            return HttpResponse("<script>alert('Please select a date and time greater than 1 hours from starting time.');window.location='../view_my_veh';</script>")
        
        cursor.execute("insert into plan values(null,'"+str(request.session['uid'])+"','"+str(id)+"','"+start+"','"+end+"','"+seats+"','"+str(input_datetime)+"','"+str(current_datetime)+"','active')")
        planid = cursor.lastrowid
        cursor.execute("insert into route values(null,'"+str(planid)+"','"+start+"','start point','1','not started','active','"+str(input_datetime)+"')")
        srid =cursor.lastrowid
        cursor.execute("insert into available_seats values(null,'"+str(planid)+"','"+str(srid)+"','"+seats+"')")
        cursor.execute("insert into route values(null,'"+str(planid)+"','"+end+"','end point','2','not started','active','"+str(input_edatetime)+"')")
        erid =cursor.lastrowid
        cursor.execute("insert into available_seats values(null,'"+str(planid)+"','"+str(erid)+"','"+seats+"')")
        return HttpResponse("<script>alert('Plan added and will be shown to the all Passengers on this site. Passengers who want to  travel through your specified route will book it. Try to maintain the time as you mentioned in the plan. Here you can add middile towns in b/w your plan and that is possible 1 hour before the time plan starts. So go ahead and add more middle towns in your route if you want ');window.location='../view_my_veh';</script>")

        # return HttpResponse("<script>alert('Plan added and will be shown to the all travellers on this site. Travellers who want to  travel will send you request and town details which they will wait and you can accept the approvel or reject it. and try to maintain the time as you mentioned in the plan and if you didint start travel in 1 hour then the plan will be aborted. here you can add middile towns in b/w your plan and that is possible 1 hour before the time plan starts. So go ahead and add more middle towns in your route if you want ');window.location='../view_my_veh';</script>")

    cursor.execute("select town_id,name from town where district_id ='1'")
    di1 = cursor.fetchall()
    d1 =[]
    for i in di1:
        a={"id":i[0], "name":i[1]}
        d1.append(a)

    cursor.execute("select town_id,name from town where district_id ='2'")
    di2 = cursor.fetchall()
    d2 =[]
    for i in di2:
        a={"id":i[0], "name":i[1]}
        d2.append(a)
    cursor.execute("select town_id,name from town where district_id ='3'")
    di3 = cursor.fetchall()
    d3 =[]
    for i in di3:
        a={"id":i[0], "name":i[1]}
        d3.append(a)
    cursor.execute("select town_id,name from town where district_id ='4'")
    di4 = cursor.fetchall()
    d4 =[]
    for i in di4:
        a={"id":i[0], "name":i[1]}
        d4.append(a)
    cursor.execute("select town_id,name from town where district_id ='5'")
    di5 = cursor.fetchall()
    d5 =[]
    for i in di5:
        a={"id":i[0], "name":i[1]}
        d5.append(a)
    cursor.execute("select town_id,name from town where district_id ='6'")
    di6 = cursor.fetchall()
    d6 =[]
    for i in di6:
        a={"id":i[0], "name":i[1]}
        d6.append(a)
    cursor.execute("select town_id,name from town where district_id ='7'")
    di7 = cursor.fetchall()
    d7 =[]
    for i in di7:
        a={"id":i[0], "name":i[1]}
        d7.append(a)
    cursor.execute("select town_id,name from town where district_id ='8'")
    di8 = cursor.fetchall()
    d8 =[]
    for i in di8:
        a={"id":i[0], "name":i[1]}
        d8.append(a)
    cursor.execute("select town_id,name from town where district_id ='9'")
    di9 = cursor.fetchall()
    d9 =[]
    for i in di9:
        a={"id":i[0], "name":i[1]}
        d9.append(a)
    cursor.execute("select town_id,name from town where district_id ='10'")
    di10 = cursor.fetchall()
    d10 =[]
    for i in di10:
        a={"id":i[0], "name":i[1]}
        d10.append(a)
    cursor.execute("select town_id,name from town where district_id ='11'")
    di11 = cursor.fetchall()
    d11 =[]
    for i in di11:
        a={"id":i[0], "name":i[1]}
        d11.append(a)
    cursor.execute("select town_id,name from town where district_id ='12'")
    di12 = cursor.fetchall()
    d12 =[]
    for i in di12:
        a={"id":i[0], "name":i[1]}
        d12.append(a)
    cursor.execute("select town_id,name from town where district_id ='13'")
    di13 = cursor.fetchall()
    d13 =[]
    for i in di13:
        a={"id":i[0], "name":i[1]}
        d13.append(a)
    cursor.execute("select town_id,name from town where district_id ='14'")
    di14 = cursor.fetchall()
    d14 =[]
    for i in di14:
        a={"id":i[0], "name":i[1]}
        d14.append(a)
    districts = {"Alappuzha": d1,"Ernakulam": d2,"Idukki": d3,"Kannur": d4,"Kasaragod": d5,"Kollam": d6,"Kottayam": d7,"Kozhikode": d8,"Malappuram": d9,"Palakkad": d10,"Pathanamthitta": d11,"Thiruvananthapuram": d12, "Thrissur": d13,"wayanad":d14}
    print(districts)
    import json
    districts_json = json.dumps(districts)
    print(districts_json)
    return render(request,'user/add_plan.html',{'districts_json':districts_json})



def view_plan(request,id):
    cursor = connection.cursor()
    cursor.execute("select * from plan where status ='active' or status = 'running'")
    aata = cursor.fetchall()
    for i in aata:
        plan_time =i[6]
        cursor.execute("select * from route where route_type='end point' and idplan ='"+str(i[0])+"' ")
        enddata=cursor.fetchone()
        end_time = enddata[7]

        import datetime
        plan_time = datetime.datetime.strptime(plan_time, '%Y-%m-%d %H:%M:%S')
        end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
        # plan_time_minus_1_hour = plan_time - datetime.timedelta(hours=1)
        # print(plan_time_minus_1_hour)
        current_datetime = datetime.datetime.now()
        if end_time >= current_datetime >= plan_time:
            cursor.execute("update plan set status ='running' where idplan='"+str(i[0])+"' ")
        if end_time < current_datetime:
            cursor.execute("update plan set status ='completed' where idplan='"+str(i[0])+"' ")
    cursor.execute("select plan.*,a.name,b.name from plan join town as a join town as b where plan.user_id ='"+str(request.session['uid'])+"' and plan.vehid='"+id+"' and plan.status ='active' and plan.start =a.town_id and plan.end =b.town_id")
    plansa = cursor.fetchall()
    cursor.execute("select plan.*,a.name,b.name from plan join town as a join town as b where plan.user_id ='"+str(request.session['uid'])+"' and plan.vehid='"+id+"' and plan.status ='running' and plan.start =a.town_id and plan.end =b.town_id")
    plansr = cursor.fetchall()
    cursor.execute("select plan.*,a.name,b.name from plan join town as a join town as b where plan.user_id ='"+str(request.session['uid'])+"' and plan.vehid='"+id+"' and plan.status ='completed' and plan.start =a.town_id and plan.end =b.town_id")
    plansc = cursor.fetchall()
    cursor.execute("select * from vehicle_register where vehicle_number='"+id+"' ")
    veh = cursor.fetchone()
    return render(request,'user/view_planv.html',{'vehicle':veh,'active':plansa,'running':plansr,'completed':plansc})


def view_route(request,id):
    cursor = connection.cursor()
    cursor.execute("select plan.*,a.name,b.name from plan join town as a join town as b where plan.user_id ='"+str(request.session['uid'])+"' and plan.idplan='"+id+"' and plan.start =a.town_id and plan.end =b.town_id")
    plansa = cursor.fetchone()
    print(plansa)
    cursor.execute("select * from vehicle_register where vehicle_number='"+plansa[2]+"' ")
    veh = cursor.fetchone()
    print(veh)
    cursor.execute("select * from route where idplan ='"+str(id)+"' and status ='active'")
    data = cursor.fetchall()
    routcount =len(data)
    print(routcount)
    s=[]
    for i in range(1,routcount):
        print(i)
        
        cursor.execute("select route.*,town.town_id,town.name from route join town  where route.route_num ='"+str(i)+"' and route.town = town.town_id and route.idplan='"+id+"'")
        a = cursor.fetchone()
        cursor.execute("select route.*,town.town_id,town.name from route join town where route.route_num ='"+str(i+1)+"' and route.town = town.town_id and route.idplan='"+id+"' ")
        b = cursor.fetchone()
        print(a)
        print(b)
        sa =(str(a[4]),str(b[4]),str(a[0]),str(b[0]),str(a[9]),str(b[9]),str(a[7]),str(b[7]))
        s.append(sa)
    s=tuple(s)
    print(s)
    request.session['viewed_planid']=str(a[1])
    return render(request,'user/view_routev.html',{'s':s,'vehicle':veh,'active':plansa})
    

def view_routec(request,id):
    cursor = connection.cursor()
    cursor.execute("select plan.*,a.name,b.name from plan join town as a join town as b where plan.user_id ='"+str(request.session['uid'])+"' and plan.idplan='"+id+"' and plan.start =a.town_id and plan.end =b.town_id")
    plansa = cursor.fetchone()
    print(plansa)
    cursor.execute("select * from vehicle_register where vehicle_number='"+plansa[2]+"' ")
    veh = cursor.fetchone()
    print(veh)
    cursor.execute("select * from route where idplan ='"+str(id)+"' and status ='active'")
    data = cursor.fetchall()
    routcount =len(data)
    print(routcount)
    s=[]
    for i in range(1,routcount):
        print(i)
        
        cursor.execute("select route.*,town.town_id,town.name from route join town  where route.route_num ='"+str(i)+"' and route.town = town.town_id and route.idplan='"+id+"'")
        a = cursor.fetchone()
        cursor.execute("select route.*,town.town_id,town.name from route join town where route.route_num ='"+str(i+1)+"' and route.town = town.town_id and route.idplan='"+id+"' ")
        b = cursor.fetchone()
        print(a)
        print(b)
        sa =(str(a[4]),str(b[4]),str(a[0]),str(b[0]),str(a[9]),str(b[9]),str(a[7]),str(b[7]))
        s.append(sa)
    s=tuple(s)
    print(s)
    request.session['viewed_planid']=str(a[1])
    return render(request,'user/view_routec.html',{'s':s,'vehicle':veh,'active':plansa})
    



def add_route(request,id):
    cursor = connection.cursor()
    cursor.execute("select plan_time from plan where idplan ='"+str(request.session['viewed_planid'])+"'")
    data = cursor.fetchone()
    plan_time =data[0]
    import datetime
    plan_time = datetime.datetime.strptime(plan_time, '%Y-%m-%d %H:%M:%S')
    plan_time_minus_1_hour = plan_time - datetime.timedelta(hours=1)
    print(plan_time_minus_1_hour)
    current_datetime = datetime.datetime.now()
    print(current_datetime)
    if current_datetime > plan_time_minus_1_hour:
        return HttpResponse("<script>alert('sorry you cant update. there is only less than 1 hour left. so be ready to start  plan on "+str(plan_time)+"');window.location='../view_my_veh';</script>")

    cursor.execute("select * from route join town join district where route.idplan ='"+str(request.session['viewed_planid'])+"' and route.route_num ='"+str(id)+"' and route.town = town.town_id and district.district_id = town.district_id ")
    routea = cursor.fetchone()
    routead =routea[13]
    routeat =routea[9]
    timea=routea[7]
    import datetime
    timeat = datetime.datetime.strptime(timea, '%Y-%m-%d %H:%M:%S')
    print(timeat)
    timeat_plus_10_minutes = timeat + datetime.timedelta(minutes=10)
    print(timeat_plus_10_minutes)
    jd = int(id)+1
    cursor.execute("select * from route join town join district where route.idplan ='"+str(request.session['viewed_planid'])+"' and route.route_num ='"+str(jd)+"' and route.town = town.town_id and district.district_id = town.district_id ")
    routeb = cursor.fetchone()
    routebd =routeb[13]
    routebt =routeb[9]
    timeb=routeb[7]
    timebt = datetime.datetime.strptime(timeb, '%Y-%m-%d %H:%M:%S')
    print(timebt)
    timebt_minus_10_minutes = timebt - datetime.timedelta(minutes=10)
    print(timebt_minus_10_minutes)

    cursor.execute("select * from plan where idplan ='"+str(request.session['viewed_planid'])+"'")
    veh = cursor.fetchone()
    vehno =veh[2]
    seats = veh[5]

    cursor.execute("select * from vehicle_register where vehicle_number ='"+str(vehno)+"'")
    data = cursor.fetchone()
    if request.method == 'POST':
        mtown = request.POST['town']
        date = request.POST['date']
        cursor.execute("select * from route where idplan='"+str(request.session['viewed_planid'])+"' and town ='"+str(mtown)+"' and status ='active' ")
        data = cursor.fetchone()
        if data==None:
            # Perform JavaScript validation on the date
            input_datetime = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M') 
            # input_dates=input_datetime.date() # Assuming datetime-local format
            if timeat_plus_10_minutes < input_datetime < timebt_minus_10_minutes:
                print("time is ok")
                cursor.execute("update route set route_num ='"+str(jd+1)+"' where idroute='"+str(routeb[0])+"'")
                cursor.execute("insert into route values(null,'"+str(request.session['viewed_planid'])+"','"+mtown+"','middle point','"+str(jd)+"','not started','active','"+str(input_datetime)+"')")
                mrid =cursor.lastrowid
                cursor.execute("insert into available_seats values(null,'"+str(request.session['viewed_planid'])+"','"+str(mrid)+"','"+seats+"')")
                return HttpResponse("<script>alert('Middile route added to the plan');window.location='../view_my_veh';</script>")
            else:    
                return HttpResponse("<script>alert('sorry selected time is not valid. Please select a date and time b/w above and below towns date and time and  there should be time gap of atleast 10 minutes.');window.location='../view_my_veh';</script>")
            

        else:    
            return HttpResponse("<script>alert('you already selected the town in Plan . Add middle towns if you want to access passengers from that middle town');window.location='../view_my_veh';</script>")
        # current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
    cursor.execute("select town_id,name from town where district_id ='1'")
    di1 = cursor.fetchall()
    d1 =[]
    for i in di1:
        a={"id":i[0], "name":i[1]}
        d1.append(a)

    cursor.execute("select town_id,name from town where district_id ='2'")
    di2 = cursor.fetchall()
    d2 =[]
    for i in di2:
        a={"id":i[0], "name":i[1]}
        d2.append(a)
    cursor.execute("select town_id,name from town where district_id ='3'")
    di3 = cursor.fetchall()
    d3 =[]
    for i in di3:
        a={"id":i[0], "name":i[1]}
        d3.append(a)
    cursor.execute("select town_id,name from town where district_id ='4'")
    di4 = cursor.fetchall()
    d4 =[]
    for i in di4:
        a={"id":i[0], "name":i[1]}
        d4.append(a)
    cursor.execute("select town_id,name from town where district_id ='5'")
    di5 = cursor.fetchall()
    d5 =[]
    for i in di5:
        a={"id":i[0], "name":i[1]}
        d5.append(a)
    cursor.execute("select town_id,name from town where district_id ='6'")
    di6 = cursor.fetchall()
    d6 =[]
    for i in di6:
        a={"id":i[0], "name":i[1]}
        d6.append(a)
    cursor.execute("select town_id,name from town where district_id ='7'")
    di7 = cursor.fetchall()
    d7 =[]
    for i in di7:
        a={"id":i[0], "name":i[1]}
        d7.append(a)
    cursor.execute("select town_id,name from town where district_id ='8'")
    di8 = cursor.fetchall()
    d8 =[]
    for i in di8:
        a={"id":i[0], "name":i[1]}
        d8.append(a)
    cursor.execute("select town_id,name from town where district_id ='9'")
    di9 = cursor.fetchall()
    d9 =[]
    for i in di9:
        a={"id":i[0], "name":i[1]}
        d9.append(a)
    cursor.execute("select town_id,name from town where district_id ='10'")
    di10 = cursor.fetchall()
    d10 =[]
    for i in di10:
        a={"id":i[0], "name":i[1]}
        d10.append(a)
    cursor.execute("select town_id,name from town where district_id ='11'")
    di11 = cursor.fetchall()
    d11 =[]
    for i in di11:
        a={"id":i[0], "name":i[1]}
        d11.append(a)
    cursor.execute("select town_id,name from town where district_id ='12'")
    di12 = cursor.fetchall()
    d12 =[]
    for i in di12:
        a={"id":i[0], "name":i[1]}
        d12.append(a)
    cursor.execute("select town_id,name from town where district_id ='13'")
    di13 = cursor.fetchall()
    d13 =[]
    for i in di13:
        a={"id":i[0], "name":i[1]}
        d13.append(a)
    cursor.execute("select town_id,name from town where district_id ='14'")
    di14 = cursor.fetchall()
    d14 =[]
    for i in di14:
        a={"id":i[0], "name":i[1]}
        d14.append(a)
    districts = {"Alappuzha": d1,"Ernakulam": d2,"Idukki": d3,"Kannur": d4,"Kasaragod": d5,"Kollam": d6,"Kottayam": d7,"Kozhikode": d8,"Malappuram": d9,"Palakkad": d10,"Pathanamthitta": d11,"Thiruvananthapuram": d12, "Thrissur": d13,"wayanad":d14}
    print(districts)
    import json
    districts_json = json.dumps(districts)
    print(districts_json)
    return render(request,'user/add_route.html',{'timea':timea,'timeb':timeb,'routeat':routeat,'routead':routead,'routebt':routebt,'routebd':routebd,'districts_json':districts_json})

def go_travel(request):
    print(request.session['uid'])
    cursor = connection.cursor()
    cursor.execute("select * from plan where status ='active' or status='running'")
    aata = cursor.fetchall()
    for i in aata:
        plan_time =i[6]
        cursor.execute("select * from route where route_type='end point' and idplan ='"+str(i[0])+"' ")
        enddata=cursor.fetchone()
        end_time = enddata[7]

        import datetime
        plan_time = datetime.datetime.strptime(plan_time, '%Y-%m-%d %H:%M:%S')
        end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
        # plan_time_minus_1_hour = plan_time - datetime.timedelta(hours=1)
        # print(plan_time_minus_1_hour)
        current_datetime = datetime.datetime.now()
        if end_time >= current_datetime >= plan_time:
            cursor.execute("update plan set status ='running' where idplan='"+str(i[0])+"' ")
        if end_time < current_datetime:
            cursor.execute("update plan set status ='completed' where idplan='"+str(i[0])+"' ")

            # return HttpResponse("<script>alert('sorry you cant update. there is only less than 1 hour left. so be ready to start  plan on "+str(plan_time)+"');window.location='../view_my_veh';</script>")



    uid = request.session['uid']
    cursor = connection.cursor()
    cursor.execute("select town_id,name from town where district_id ='1'")
    di1 = cursor.fetchall()
    d1 =[]
    for i in di1:
        a={"id":i[0], "name":i[1]}
        d1.append(a)

    cursor.execute("select town_id,name from town where district_id ='2'")
    di2 = cursor.fetchall()
    d2 =[]
    for i in di2:
        a={"id":i[0], "name":i[1]}
        d2.append(a)
    cursor.execute("select town_id,name from town where district_id ='3'")
    di3 = cursor.fetchall()
    d3 =[]
    for i in di3:
        a={"id":i[0], "name":i[1]}
        d3.append(a)
    cursor.execute("select town_id,name from town where district_id ='4'")
    di4 = cursor.fetchall()
    d4 =[]
    for i in di4:
        a={"id":i[0], "name":i[1]}
        d4.append(a)
    cursor.execute("select town_id,name from town where district_id ='5'")
    di5 = cursor.fetchall()
    d5 =[]
    for i in di5:
        a={"id":i[0], "name":i[1]}
        d5.append(a)
    cursor.execute("select town_id,name from town where district_id ='6'")
    di6 = cursor.fetchall()
    d6 =[]
    for i in di6:
        a={"id":i[0], "name":i[1]}
        d6.append(a)
    cursor.execute("select town_id,name from town where district_id ='7'")
    di7 = cursor.fetchall()
    d7 =[]
    for i in di7:
        a={"id":i[0], "name":i[1]}
        d7.append(a)
    cursor.execute("select town_id,name from town where district_id ='8'")
    di8 = cursor.fetchall()
    d8 =[]
    for i in di8:
        a={"id":i[0], "name":i[1]}
        d8.append(a)
    cursor.execute("select town_id,name from town where district_id ='9'")
    di9 = cursor.fetchall()
    d9 =[]
    for i in di9:
        a={"id":i[0], "name":i[1]}
        d9.append(a)
    cursor.execute("select town_id,name from town where district_id ='10'")
    di10 = cursor.fetchall()
    d10 =[]
    for i in di10:
        a={"id":i[0], "name":i[1]}
        d10.append(a)
    cursor.execute("select town_id,name from town where district_id ='11'")
    di11 = cursor.fetchall()
    d11 =[]
    for i in di11:
        a={"id":i[0], "name":i[1]}
        d11.append(a)
    cursor.execute("select town_id,name from town where district_id ='12'")
    di12 = cursor.fetchall()
    d12 =[]
    for i in di12:
        a={"id":i[0], "name":i[1]}
        d12.append(a)
    cursor.execute("select town_id,name from town where district_id ='13'")
    di13 = cursor.fetchall()
    d13 =[]
    for i in di13:
        a={"id":i[0], "name":i[1]}
        d13.append(a)
    cursor.execute("select town_id,name from town where district_id ='14'")
    di14 = cursor.fetchall()
    d14 =[]
    for i in di14:
        a={"id":i[0], "name":i[1]}
        d14.append(a)
    districts = {"Alappuzha": d1,"Ernakulam": d2,"Idukki": d3,"Kannur": d4,"Kasaragod": d5,"Kollam": d6,"Kottayam": d7,"Kozhikode": d8,"Malappuram": d9,"Palakkad": d10,"Pathanamthitta": d11,"Thiruvananthapuram": d12, "Thrissur": d13,"wayanad":d14}
    print(districts)
    import json
    districts_json = json.dumps(districts)
    print(districts_json)


    cursor = connection.cursor()
    cursor.execute("select plan.*,a.name,b.name from plan join town as a join town as b where  plan.status ='active' and plan.start =a.town_id and plan.end =b.town_id")
    plansa = cursor.fetchall()
    # cursor.execute("select * from vehicle_register where vehicle_number='"+id+"' ")
    # veh = cursor.fetchone()

    return render(request,'user/go_travel.html',{'districts_json':districts_json,'active':plansa})


def view_routes(request,id):
    print(request.session['uid'],"userid")
    cursor = connection.cursor()
    cursor.execute("select plan.*,a.name,b.name from plan join town as a join town as b where plan.idplan='"+id+"' and plan.status ='active' and plan.start =a.town_id and plan.end =b.town_id")
    plansa = cursor.fetchone()
    print(plansa)
    cursor.execute("select * from vehicle_register where vehicle_number='"+plansa[2]+"' ")
    veh = cursor.fetchone()
    print(veh)
    if request.method =='POST':
        stown = request.POST['stown']
        etown = request.POST['etown']
        print(etown)
        if stown == etown:
            return HttpResponse("<script>alert('You selected the same town as start and end point. Please select different towns.'); window.location='../view_routes/%s';</script>" % id)
        cursor.execute("select * from route join town join district where  route.idplan ='"+str(id)+"' and route.town ='"+stown+"'and route.town = town.town_id and town.district_id = district.district_id ")
        sdata =cursor.fetchone()
        sroute_num = sdata[4]
        stownname=sdata[9]
        stime=sdata[7]
        sdist=sdata[13]
        cursor.execute("select * from route join town join district where  route.idplan ='"+str(id)+"' and route.town ='"+etown+"' and route.town = town.town_id and town.district_id = district.district_id")
        edata =cursor.fetchone()
        eroute_num = edata[4]
        etownname=edata[9]
        etime=edata[7]
        edist=edata[13]
        rc=[]
        for i in range(int(sroute_num),int(eroute_num)+1):
            cursor.execute("select * from route where route_num='"+str(i)+"' and idplan='"+str(id)+"'")
            sea =cursor.fetchone()
            cursor.execute("select * from available_seats where pid='"+str(id)+"' and rid ='"+str(sea[0])+"'")
            se=cursor.fetchone()
            rc.append(int(se[3]))
        avail_seats=int(min(rc))
        print(avail_seats)
        if avail_seats<=0:
            return HttpResponse("<script>alert('No seats available'); window.location='../view_routes/%s';</script>" % id)

        print(request.session['uid'],"userid")
        return render(request,'user/book_route.html',{'sroute':sdata[0],'eroute':edata[0],'id':id,'avail_seats':avail_seats,'sdist':sdist,'edist':edist,'stown':stown,'etown':etown,'sname':stownname,'ename':etownname,'stime':stime,'etime':etime,'vehicle':veh,'active':plansa})
  
    
    cursor.execute("select * from route where idplan ='"+str(id)+"' and status ='active'")
    data = cursor.fetchall()
    routcount =len(data)
    print(routcount)
    s=[]
    for i in range(1,routcount):
        print(i)
        
        cursor.execute("select route.*,town.town_id,town.name from route join town  where route.route_num ='"+str(i)+"' and route.town = town.town_id and route.idplan='"+id+"'")
        a = cursor.fetchone()
        cursor.execute("select route.*,town.town_id,town.name from route join town where route.route_num ='"+str(i+1)+"' and route.town = town.town_id and route.idplan='"+id+"'")
        b = cursor.fetchone()
        print(a)
        print(b)
        sa =(str(a[4]),str(b[4]),str(a[0]),str(b[0]),str(a[9]),str(b[9]),str(a[7]),str(b[7]),a[2],b[2])
        s.append(sa)
    s=tuple(s)
    print(s)
    request.session['viewed_planids']=str(a[1])
    cursor.execute("select * from user_register where user_id='"+str(plansa[1])+"'")
    owner = cursor.fetchone()
    return render(request,'user/view_routes.html',{'s':s,'vehicle':veh,'active':plansa,'owner':owner})

def book_travel(request,id):
    if request.method=='POST':
        cursor = connection.cursor()
        vehno = request.POST['vehno']
        vehuser = request.POST['vehuser']
        seat = request.POST['seats']
        sroute=request.POST['sroute']
        eroute=request.POST['eroute']
        stime=request.POST['stime']
        etime=request.POST['etime']
        uid = str(request.session['uid'])
        print(vehuser,"vehuser")
        print(uid,"userid")
        if uid == str(vehuser):
            print(1)
            return HttpResponse("<script>alert('its your plan so you cant book.. ');window.location='../userhome';</script>")
        else:
            
            import datetime
            from datetime import timedelta
            current_datetime = datetime.datetime.now()
            cursor.execute("insert into  travel_booking values(null,'"+str(id)+"','"+str(sroute)+"','"+str(stime)+"','"+str(eroute)+"','"+str(etime)+"','"+str(seat)+"','"+str(uid)+"',curdate())")

            cursor.execute("select * from route  where idroute='"+str(sroute)+"'")
            sdata =cursor.fetchone()
            sroute_num = sdata[4]
            cursor.execute("select * from route  where idroute='"+str(eroute)+"'")
            edata =cursor.fetchone()
            eroute_num = edata[4]
            
            for i in range(int(sroute_num),int(eroute_num)+1):
                cursor.execute("select * from route where route_num='"+str(i)+"' and idplan='"+str(id)+"'")
                sea =cursor.fetchone()
                cursor.execute("select * from available_seats where pid='"+str(id)+"' and rid ='"+str(sea[0])+"'")
                se=cursor.fetchone()
                a =int(se[3])-int(seat)
                cursor.execute("update available_seats set seats ='"+str(a)+"'  where pid='"+str(id)+"' and rid ='"+str(sea[0])+"'")
            
            return HttpResponse("<script>alert('Seats Booked.. ');window.location='../userhome';</script>")

def travel_bookings(request):
    cursor = connection.cursor()
    cursor.execute("select * from plan where status ='active' or status='running'")
    aata = cursor.fetchall()
    for i in aata:
        plan_time =i[6]
        cursor.execute("select * from route where route_type='end point' and idplan ='"+str(i[0])+"' ")
        enddata=cursor.fetchone()
        end_time = enddata[7]

        import datetime
        plan_time = datetime.datetime.strptime(plan_time, '%Y-%m-%d %H:%M:%S')
        end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
        # plan_time_minus_1_hour = plan_time - datetime.timedelta(hours=1)
        # print(plan_time_minus_1_hour)
        current_datetime = datetime.datetime.now()
        if end_time >= current_datetime >= plan_time:
            cursor.execute("update plan set status ='running' where idplan='"+str(i[0])+"' ")
        if end_time < current_datetime:
            cursor.execute("update plan set status ='completed' where idplan='"+str(i[0])+"' ")

            # return HttpResponse("<script>alert('sorry you cant update. there is only less than 1 hour left. so be ready to start  plan on "+str(plan_time)+"');window.location='../view_my_veh';</script>")


    uid = request.session['uid']
    cursor = connection.cursor()
    cursor.execute("select * from travel_booking join plan where travel_booking.user_id='"+str(uid)+"'and plan.status ='active' and travel_booking.idplan =plan.idplan ")
    data = cursor.fetchall()
    bookings=[]
    for i in data:
        cursor.execute("select plan.*,a.name,b.name from plan join town as a join town as b where plan.idplan='"+i[1]+"' and  plan.start =a.town_id and plan.end =b.town_id")
        plansa = cursor.fetchone()
        a=plansa[9]
        b=plansa[10]
        cursor.execute("select * from vehicle_register where vehicle_number='"+plansa[2]+"' ")
        veh = cursor.fetchone()
        c=veh[0]
        d=veh[3]
        cursor.execute("select * from user_register where user_id='"+str(veh[1])+"' ")
        owner = cursor.fetchone()
        m=owner[1]
        n=owner[3]
        o=owner[4]
        cursor.execute("select * from route  where idroute='"+i[2]+"'")
        sdata = cursor.fetchone()
        stown =sdata[2]
        cursor.execute("select * from town join district where town.town_id='"+stown+"' and town.district_id = district.district_id")
        stowndetail=cursor.fetchone()
        e = stowndetail[1]
        f = stowndetail[5]
        g = sdata[7]

        cursor.execute("select * from route  where idroute='"+i[4]+"'")
        edata = cursor.fetchone()
        etown =edata[2]
        cursor.execute("select * from town join district where town.town_id='"+etown+"' and town.district_id = district.district_id")
        etowndetail=cursor.fetchone()
        h =etowndetail[1]
        j = etowndetail[5]
        k = edata[7]
        l= i[6]
        p=i[8]
        book = (a,b,c,d,e,f,g,h,j,k,l,m,n,o,p)
        bookings.append(book)
    booking=tuple(bookings)

    cursor.execute("select * from travel_booking join plan where travel_booking.user_id='"+str(uid)+"'and plan.status ='running' and travel_booking.idplan =plan.idplan ")
    data = cursor.fetchall()
    bookings=[]
    for i in data:
        cursor.execute("select plan.*,a.name,b.name from plan join town as a join town as b where plan.idplan='"+i[1]+"' and  plan.start =a.town_id and plan.end =b.town_id")
        plansa = cursor.fetchone()
        a=plansa[9]
        b=plansa[10]
        cursor.execute("select * from vehicle_register where vehicle_number='"+plansa[2]+"' ")
        veh = cursor.fetchone()
        c=veh[0]
        d=veh[3]
        cursor.execute("select * from user_register where user_id='"+str(veh[1])+"' ")
        owner = cursor.fetchone()
        m=owner[1]
        n=owner[3]
        o=owner[4]
        cursor.execute("select * from route  where idroute='"+i[2]+"'")
        sdata = cursor.fetchone()
        stown =sdata[2]
        cursor.execute("select * from town join district where town.town_id='"+stown+"' and town.district_id = district.district_id")
        stowndetail=cursor.fetchone()
        e = stowndetail[1]
        f = stowndetail[5]
        g = sdata[7]

        cursor.execute("select * from route  where idroute='"+i[4]+"'")
        edata = cursor.fetchone()
        etown =edata[2]
        cursor.execute("select * from town join district where town.town_id='"+etown+"' and town.district_id = district.district_id")
        etowndetail=cursor.fetchone()
        h =etowndetail[1]
        j = etowndetail[5]
        k = edata[7]
        l= i[6]
        p=i[8]
        book = (a,b,c,d,e,f,g,h,j,k,l,m,n,o,p)
        bookings.append(book)
    rbooking=tuple(bookings)

    cursor.execute("select * from travel_booking join plan where travel_booking.user_id='"+str(uid)+"'and plan.status ='completed' and travel_booking.idplan =plan.idplan ")
    data = cursor.fetchall()
    bookings=[]
    for i in data:
        cursor.execute("select plan.*,a.name,b.name from plan join town as a join town as b where plan.idplan='"+i[1]+"' and  plan.start =a.town_id and plan.end =b.town_id")
        plansa = cursor.fetchone()
        a=plansa[9]
        b=plansa[10]
        cursor.execute("select * from vehicle_register where vehicle_number='"+plansa[2]+"' ")
        veh = cursor.fetchone()
        c=veh[0]
        d=veh[3]
        cursor.execute("select * from user_register where user_id='"+str(veh[1])+"' ")
        owner = cursor.fetchone()
        m=owner[1]
        n=owner[3]
        o=owner[4]
        cursor.execute("select * from route  where idroute='"+i[2]+"'")
        sdata = cursor.fetchone()
        stown =sdata[2]
        cursor.execute("select * from town join district where town.town_id='"+stown+"' and town.district_id = district.district_id")
        stowndetail=cursor.fetchone()
        e = stowndetail[1]
        f = stowndetail[5]
        g = sdata[7]

        cursor.execute("select * from route  where idroute='"+i[4]+"'")
        edata = cursor.fetchone()
        etown =edata[2]
        cursor.execute("select * from town join district where town.town_id='"+etown+"' and town.district_id = district.district_id")
        etowndetail=cursor.fetchone()
        h =etowndetail[1]
        j = etowndetail[5]
        k = edata[7]
        l= i[6]
        p=i[8]
        q=plansa[0]
        book = (a,b,c,d,e,f,g,h,j,k,l,m,n,o,p,q)
        bookings.append(book)
    cbooking=tuple(bookings)



        
    return render(request,'user/view_bookings.html',{'data':booking,'rdata':rbooking,'cdata':cbooking})
def view_feedback(request,id):
    cursor = connection.cursor()
    cursor.execute("select * from feedback join user_register where pid='"+str(id)+"' and feedback.user_id = user_register.user_id")
    data = cursor.fetchall()
    cursor.execute("select plan.*,a.name,b.name from plan join town as a join town as b where plan.idplan='"+id+"' and  plan.start =a.town_id and plan.end =b.town_id")
    plansa = cursor.fetchone()
    cursor.execute("select * from vehicle_register where vehicle_number='"+plansa[2]+"' ")
    veh = cursor.fetchone()
    return render(request,'user/view_feedback.html',{'data':data,'active':plansa,'vehicle':veh,'id':id})

def oview_feedback(request,id):
    cursor = connection.cursor()
    cursor.execute("select * from feedback join user_register where pid='"+str(id)+"' and feedback.user_id = user_register.user_id")
    data = cursor.fetchall()
    cursor.execute("select plan.*,a.name,b.name from plan join town as a join town as b where plan.idplan='"+id+"' and  plan.start =a.town_id and plan.end =b.town_id")
    plansa = cursor.fetchone()
    cursor.execute("select * from vehicle_register where vehicle_number='"+plansa[2]+"' ")
    veh = cursor.fetchone()
    return render(request,'user/oview_feedback.html',{'data':data,'active':plansa,'vehicle':veh,'id':id})

def aview_feedback(request,id):
    cursor = connection.cursor()
    cursor.execute("select * from feedback join user_register where pid='"+str(id)+"' and feedback.user_id = user_register.user_id")
    data = cursor.fetchall()
    cursor.execute("select plan.*,a.name,b.name from plan join town as a join town as b where plan.idplan='"+id+"' and  plan.start =a.town_id and plan.end =b.town_id")
    plansa = cursor.fetchone()
    cursor.execute("select * from vehicle_register where vehicle_number='"+plansa[2]+"' ")
    veh = cursor.fetchone()
    return render(request,'admin/oview_feedback.html',{'data':data,'active':plansa,'vehicle':veh,'id':id})

def add_feedback(request,id):
    cursor = connection.cursor()
    if request.method=='POST':
        userid=request.session['uid']
        feedback = request.POST['feedback']
        cursor.execute("select * from feedback where user_id='"+str(userid)+"' and feedback_details='"+feedback+"' and pid='"+str(id)+"'")
        data = cursor.fetchone()
        if data ==None:
            cursor.execute("insert into feedback values(null,'"+str(userid)+"','"+feedback+"',curdate(),'"+str(id)+"')")
            return redirect(view_feedback,id=id)
    cursor.execute("select plan.*,a.name,b.name from plan join town as a join town as b where plan.idplan='"+id+"'  and plan.start =a.town_id and plan.end =b.town_id")
    plansa = cursor.fetchone()
    cursor.execute("select * from vehicle_register where vehicle_number='"+plansa[2]+"' ")
    veh = cursor.fetchone()
    return render(request,'user/add_feedback.html',{'active':plansa,'vehicle':veh,'id':id})



def view_dbookings(request,id):
    cursor = connection.cursor()
    cursor.execute("select * from plan where idplan='"+id+"'")
    data = cursor.fetchone()
    vehno=data[2]
    cursor.execute("select * from travel_booking where idplan = '"+id+"' ")
    data = cursor.fetchone()
    if data==None:
            return HttpResponse("<script>alert('No Bookings'); window.location='../view_plan/%s';</script>" % vehno)
    cursor.execute("select u.name,u.phone,u.email,dia.name,ta.name,t.stime,dib.name,tb.name,t.etime,t.seats,t.booked_time from travel_booking as t join route as ra join route as rb join town as ta join town as tb join district as dia join district as dib join user_register as u where t.idplan = '"+id+"' and t.start = ra.idroute and t.end = rb.idroute and ra.town = ta.town_id and rb.town = tb.town_id and ta.district_id = dia.district_id and tb.district_id = dib.district_id and t.user_id = u.user_id ")
    data =cursor.fetchall()
    print(data,"data")
    return render(request,'user/view_dbookings.html',{'data':data})



# def update_profile(request):
#     if request.method == 'POST':
#         name = request.POST['name']
#         address = request.POST['address']
#         email = request.POST['email']
#         cursor = connection.cursor()
#         cursor.execute("update login set name ='"+str(name)+"', address ='"+str(address)+"', email ='"+str(email)+"' where admin_id ='admin' ")
#         return redirect(admin_profile)
#     else:
#         cursor = connection.cursor()
#         cursor.execute("select * from login")
#         data = cursor.fetchone()
#         return render(request, 'traffic/update_profile.html',{'data':data})

# def change_password(request):
    # if request.method == 'POST':
    #     old = request.POST['old_password']
    #     new = request.POST['new_password']
    #     conform = request.POST['conform_password']
    #     # longitude = request.POST['longitude']
    #     cursor = connection.cursor()
    #     cursor.execute("select password from login where admin_id = 'admin' ")
    #     password =cursor.fetchone()
    #     print(password[0])
    #     if password[0] == old:
    #         if new == conform:
    #             cursor.execute("update login set password ='"+str(conform)+"' where admin_id ='admin' ")
    #             return redirect(admin_profile)
    #         else:
    #             return HttpResponse("<script>alert('please enter same new password  in conform password');window.location='../adminprofile';</script>")
    #     else:
    #         return HttpResponse("<script>alert('incorrect password please validate ');window.location='../adminprofile';</script>")


    # else:
    #     return render(request,'traffic/change_password.html')