from django.shortcuts import render, redirect, get_object_or_404
from apps.models import *
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.decorators.cache import never_cache
from datetime import datetime
from apps.decorators import role_required
from django.views.decorators.cache import cache_control
from django.db.models import Count
from django.utils import timezone

# ===================== LOGIN =====================
def login_page(request):

    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            if user.role == 1:
                return redirect('/admin_dashboard/')
            elif user.role == 2:
                return redirect('/hr_dashboard/')
            elif user.role == 3:
                return redirect('/employee_dashboard/')

        messages.error(request, "Invalid username or password")

    return render(request, 'login.html')


# ===================== SIGN UP =====================
def sign_up(request):

    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role")

        user = UsersData(
            username=username,
            email=email,
            role=role
        )
        user.set_password(password)
        user.save()

        return redirect("/login/")

    return render(request, 'sign_up.html')


# ===================== ADMIN DASHBOARD =====================
@never_cache
@login_required(login_url='/login/')
@role_required(['1' ])
def admin_dashboard(request):
    return render(request, "admin_dashboard.html")


# ===================== rewards =====================
@never_cache
@login_required(login_url='/login/')
@role_required(['1' , '2'])
def admin_rewards(request):

    current_month = datetime.now().month
    selected_month = int(request.GET.get("month", current_month))

    # ✅ Get all active employees
    employees = UsersData.objects.filter(role=3).exclude(is_active=0)

    # ✅ Get performance for selected month (DICT for fast lookup)
    performance_map = {
        p.user_id: p.performance_score
        for p in Performance.objects.filter(month=selected_month)
    }

    # ✅ CALCULATE REWARD FOR EACH EMPLOYEE
    for emp in employees:
        base = performance_map.get(emp.id, 0)   # ✅ From Performance table
        bonus = emp.bonus_points or 0            # ✅ From UsersData

        
       

    # ✅ PAGINATION (AFTER CALCULATION)
    paginator = Paginator(employees, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    

    
    

    return render(request , "admin_rewards.html" , {"employees":page_obj , "current_month":current_month , "selected_month": selected_month ,"base":base , "bonus":bonus })


# ===================== performance =====================
@never_cache
@login_required(login_url='/login/')
@role_required(['1' , '2'])
def admin_performance (request):

    current_month = datetime.now().month
    selected_month = int(request.GET.get("month", current_month))

    employees = UsersData.objects.filter(role=3).values_list('id', flat=True)

    performances = (Performance.objects.select_related("user").filter(employee_id__in=employees, month=selected_month))

    paginator = Paginator(performances, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request , "admin_performance.html" , {"performances":page_obj})


# ===================== voting list =====================
@never_cache
@login_required(login_url='/login/')
@role_required(['1' , '2'])
def admin_voting(request):

    current_month = datetime.now().month
    selected_month = int(request.GET.get("month", current_month))

    votes = (
    PeerVoting.objects
    .select_related("vote_for")
    .filter(month=selected_month, vote=1)
    .values("vote_for__first_name", "vote_for__email")
    .annotate(total_votes=Count("id"))
    .order_by("-total_votes"))


    paginator = Paginator(votes, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

      
    


    return render(request, "admin_voting.html", {"votes": page_obj,"current_month":current_month})

   
# ===================== employee MANAGEMENT =====================
@never_cache
@login_required(login_url='/login/')
@role_required(['1'])
def emp_management(request):

    emp_obj = UsersData.objects.filter(role__in=[2, 3]).only(
        "id", "first_name", "last_name", "email", "username"
    ).exclude(is_active = 0)

    return render(request, "hr_management.html", {"emp_obj": emp_obj})


# ===================== EDIT  =====================
@never_cache
@login_required(login_url='/login/')
@role_required(['1'])
def edit(request, id):

    emp = get_object_or_404(UsersData, pk=id)

    if request.method == 'POST':
        emp.first_name = request.POST.get("first_name")
        emp.username = request.POST.get("username")
        emp.email = request.POST.get("email")
        password = request.POST.get("password")

        if password:
            emp.set_password(password)

        emp.save()
        messages.success(request, "Updated successfully")

    return render(request, "edit_hr.html", {"emp": emp})


# ===================== DELETE =====================
@never_cache
@login_required(login_url='/login/')
@role_required(['1'])
def delete(request, id):

    emp = get_object_or_404(UsersData, pk=id)

    if request.method == 'POST':
        emp.is_active = 0
        emp.save()
        return redirect("/admin_dashboard/")

    return render(request, "delete_hr.html", {"emp": emp})


# ===================== ACTIVITY LOGS =====================
@never_cache
@login_required(login_url='/login/')
@role_required(['1'])
def activity_logs(request):

    logs = ActivityLog.objects.select_related("user").order_by("-created_at")

    paginator = Paginator(logs, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "activity_logs.html", {"logs": page_obj})


# ===================== CREATE HR =====================
@never_cache
@login_required(login_url='/login/')
@role_required(['1'])
def create_hr(request):

    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = UsersData(
            username=username,
            email=email,
            role=2
        )
        user.set_password(password)
        user.save()

        return redirect("/admin_dashboard/")

    return render(request, "create_hr.html")


# ===================== HR DASHBOARD =====================
@never_cache
@login_required(login_url='/login/')
@role_required(['2'])
def hr_dashboard(request):
    user = request.user
    hr_details = UsersData.objects.filter(role=2,pk = user.id ).first()
    employees = UsersData.objects.filter(role=3).only("id", "first_name", "email").exclude(is_active = 0)

    current_month = datetime.now().month
    selected_month = int(request.GET.get("month",current_month))

    


   
    if request.method == "POST" and "save_single" in request.POST:

        emp_id = request.POST.get("save_single")
        vote_id = request.POST.get(f"vote_id_{emp_id}")
        vote_undo = request.POST.get(f"vote_undo{emp_id}")

        emp = UsersData.objects.get(pk=emp_id)

        if vote_undo:
            PeerVoting.objects.filter(
                user=request.user,
                vote_for=emp,
                month=selected_month
            ).delete()

        
        if vote_id:
            emp_vote = UsersData.objects.get(pk=vote_id)

            vote_count = PeerVoting.objects.filter(
                user=request.user,
                month=selected_month,
                vote=1
            ).count()

            if vote_count >= 3:
                messages.error(request, "You can only vote for 3 employees per month.")
            else:
                already_voted = PeerVoting.objects.filter(
                    user=request.user,
                    vote_for=emp_vote,
                    month=selected_month,
                    vote=1
                ).exists()

                if already_voted:
                    messages.warning(
                        request,
                        f"You already voted for {emp_vote.first_name} this month."
                    )
                else:
                    PeerVoting.objects.create(
                        user=request.user,
                        vote_for=emp_vote,
                        month=selected_month,
                        vote=1
                    )

        return redirect("/hr_dashboard/")

 
    page_number = request.GET.get("page", 1)
    paginator_all = Paginator(employees, 8)
    page_obj = paginator_all.get_page(page_number)

    
    employees = UsersData.objects.filter(role=3).exclude(is_active = 0)
   



    voted_ids = set(
        PeerVoting.objects.filter(
            user=request.user,
            month=selected_month,
            vote=1
        ).values_list("vote_for_id", flat=True)
    )

    return render(
        request,
        "hr_dashboard.html",
        {
            "hr_details": hr_details,
            "page_obj": page_obj,
            "selected_month": selected_month,
            "voted_ids": list(voted_ids),
            "current_month":current_month
        }
    )


# ===================== ADD EMPLOYEE =====================
@never_cache
@login_required(login_url='/login/')
@role_required(['2', '1'])
def add_employee(request):

    current_month = datetime.now().month

    if request.method == 'POST':
        name = request.POST.get("first_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if UsersData.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("/add_employee/")

        if UsersData.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("/add_employee/")

        user = UsersData(
            first_name=name,
            username=username,
            email=email,
            role=3
        )
        user.set_password(password)
        user.save()

        messages.success(request, "Employee added successfully")
        return redirect("/employee_list/")

    return render(request, 'add_employee.html',{"current_month":current_month })


# ===================== EMPLOYEE LIST =====================
@never_cache
@login_required(login_url='/login/')
@role_required(['2', '1'])
def employee_list(request):

    current_month = datetime.now().month

    employees = UsersData.objects.filter(role=3).only(
        "id", "first_name", "email", "username"
    ).exclude(is_active = 0)

    return render(request, "employee_list.html", {"employees": employees ,"current_month":current_month })


# ===================== EDIT EMPLOYEE =====================
@never_cache
@login_required(login_url='/login/')
@role_required(['2', '1'])
def edit_employee(request, id):

    employee = get_object_or_404(UsersData, pk=id)

    if request.method == 'POST':
        employee.first_name = request.POST.get("first_name")
        employee.username = request.POST.get("username")
        employee.email = request.POST.get("email")

        password = request.POST.get("password")
        if password:
            employee.set_password(password)

        employee.save()
        messages.success(request, "Employee updated successfully")
        return redirect("/employee_list/")

    return render(request, "edit_employee.html", {"employee": employee})


# ===================== DELETE EMPLOYEE =====================
@never_cache
@login_required(login_url='/login/')
@role_required(['2', '1'])
def delete_employee(request, id):

    employee = get_object_or_404(UsersData, pk=id)

    if request.method == 'POST':
        employee.is_active = 0
        employee.save()
        return redirect("/employee_list/")

    return render(request, "delete_employee.html", {"employee": employee})


# ===================== EMPLOYEE DASHBOARD =====================
@never_cache
@login_required(login_url='/login/')
@role_required(['3'])
def employee_dashboard(request):

    user = request.user
    current_month = datetime.now().month


    
    
    employees = (
        UsersData.objects
        .filter(role=3)
        .exclude(id=user.id)
        .select_related()
    ).exclude(is_active = 0)

    #  Votes RECEIVED by this user
    votes_received = PeerVoting.objects.filter(
        vote_for_id=user.id,
        month=current_month
    ).count()

    #  Votes GIVEN by this user
    voted_ids = list(
        PeerVoting.objects.filter(
            user=user,
            month=current_month,
        )
        .values_list('vote_for_id', flat=True)
    )

    #  Handle POST: Vote + Undo
    if request.method == "POST":

        voted_id = request.POST.getlist("vote_ids")

        if len(voted_id) > 3:
            messages.error(request, "You can only vote for 3 employees.")
            return redirect(request.path)

        for emp_id in voted_id:
            PeerVoting.objects.get_or_create(
                user=user,
                vote_for_id=emp_id,
                month=current_month,
                defaults={"vote": 1}
            )

        undo_votes = request.POST.getlist("undo_votes")
        if undo_votes:
            PeerVoting.objects.filter(
                user=user,
                vote_for_id__in=undo_votes,
                month=current_month,
            ).delete()

        return redirect(request.path)

    

    total_employee = UsersData.objects.filter(role=3).count()

    # ===================== REWARD CALC =====================
   

    total_employee = UsersData.objects.filter(role=3).count()
    emp = UsersData.objects.filter(pk = user.id).first()
    
    # Bonus calculation
    if total_employee > 0:

        vote_ratio = votes_received / total_employee   

        if vote_ratio == 1:                 
            bonus_points = 5
            emp.bonus_points = bonus_points
            emp.save()

        elif 0.99 <= vote_ratio >= 0.75:            
            bonus_points = 4
            emp.bonus_points = bonus_points
            emp.save()

        elif 0.75 <= vote_ratio >= 0.50:            
            bonus_points = 3
            emp.bonus_points = bonus_points
            emp.save()

        elif 0.50 <= vote_ratio >= 0.25:            
            bonus_points = 2
            emp.bonus_points = bonus_points
            emp.save()

        else:                               
            bonus_points = 1
            emp.bonus_points = bonus_points
            emp.save()

    else:
        bonus_points = 1

    
    # Safe Final Score Calculation
    

    base_score = Performance.objects.filter(employee_id=user.id).first()

    performance_value = base_score.performance_score if base_score else 0

    final_score = round((performance_value * 0.7) + (bonus_points * 3), 2)


        
    slab = Rewards.objects.latest("id")  


    if slab.from_score_1 <= final_score <= slab.to_score_1:
        reward_amount = slab.reward_amount_1

    elif slab.from_score_2 <= final_score <= slab.to_score_2:
        reward_amount = slab.reward_amount_2

    elif slab.from_score_3 <= final_score <= slab.to_score_3:
        reward_amount = slab.reward_amount_3

    elif slab.from_score_4 <= final_score <= slab.to_score_4:
        reward_amount = slab.reward_amount_4

    else:
        reward_amount = 0   


    print(reward_amount)

    # Save reward to the logged-in user
    rewards = UsersData.objects.filter(pk=user.id).first()
    rewards.amount = reward_amount
    rewards.save()



    # Pagination
    page_number = request.GET.get("page", 1)
    paginator_all = Paginator(employees, 8)
    page_obj = paginator_all.get_page(page_number)

    reward = UsersData.objects.filter(pk = user.id).first()
    return render(
        request,
        "employee_dashboard.html",
        {
            "employees": page_obj,
            "votes_received": votes_received,
            "voted_ids": voted_ids,
            "reward_amount": reward,
            "selected_month":current_month
        },
    )

# ===================== logout =====================
def user_logout(request):

    if request.method == 'POST':
                
                logout(request)
                return redirect("/login/")

    return render(request, 'login.html')


# ===================== error page =====================
def error(request):

    return render(request , "error.html")

# ===================== reward management =====================
@never_cache
@login_required(login_url='/login/')
@role_required(['1'])
def reward_management(request):

    if request.method == "POST":

        from_score_1 = int(request.POST.get("from_1", 0))
        to_score_1 = int(request.POST.get("to_1", 0))
        reward_amount_1 = int(request.POST.get("price_1", 0))

        from_score_2 = int(request.POST.get("from_2", 0))
        to_score_2 = int(request.POST.get("to_2", 0))
        reward_amount_2 = int(request.POST.get("price_2", 0))

        from_score_3 = int(request.POST.get("from_3", 0))
        to_score_3 = int(request.POST.get("to_3", 0))
        reward_amount_3 = int(request.POST.get("price_3", 0))

        from_score_4 = int(request.POST.get("from_4", 0))
        to_score_4 = int(request.POST.get("to_4", 0))
        reward_amount_4 = int(request.POST.get("price_4", 0))

        

        Rewards.objects.create(
            from_score_1=from_score_1,
            to_score_1=to_score_1,
            reward_amount_1=reward_amount_1,

            from_score_2=from_score_2,
            to_score_2=to_score_2,
            reward_amount_2=reward_amount_2,

            from_score_3=from_score_3,
            to_score_3=to_score_3,
            reward_amount_3=reward_amount_3,

            from_score_4=from_score_4,
            to_score_4=to_score_4,
            reward_amount_4=reward_amount_4,
        )

        messages.success(request, "Reward slabs saved successfully!")

    
    slabs = Rewards.objects.all().order_by("-id")
    page_number = request.GET.get("page", 1)

    paginator_all = Paginator(slabs, 1)  
    page_obj = paginator_all.get_page(page_number)

    return render(request, "reward_management.html", {
        "slabs": page_obj
    })


# ===================== performance =====================
@never_cache
@login_required(login_url='/login/')
@role_required(['2'])
def performance(request):

    current_month = datetime.now().month

    selected_month = request.GET.get("month", current_month)

    employees = UsersData.objects.filter(role=3).exclude(is_active = 0)
    
    performance_map = dict(
    Performance.objects.filter(month=selected_month)
    .values_list("user_id", "performance_score"))

    monthly_data = [
        
        {
            "employee": emp,
            "score": performance_map.get(emp.id)
        }
        for emp in employees
        
    ]




    s_page = request.GET.get("s_page", 1)
    paginator_summary = Paginator(monthly_data, 10)
    page_monthly = paginator_summary.get_page(s_page)


     #  SAVE INDIVIDUAL SUMMARY SCORE (MONTHLY SUMMARY UPDATE BUTTON)
    if request.method == "POST" and "save_single" in request.POST:

        emp_id = request.POST.get("save_single")

        print(emp_id)

        # Fetch the employee
        emp = UsersData.objects.get(pk=emp_id)

        # Get score from input field
        score = request.POST.get(f"score_{emp_id}")

        if score :
            Performance.objects.update_or_create(
                user=emp,
                month=selected_month,
                defaults={
                    "performance_score": score,
                    "employee_id": emp_id,
                }
            )

            messages.success(
                request,
                f"Score updated successfully for {emp.first_name}."
            )
        else:
            messages.error(request, "Invalid score. Please enter a number between 0–100.")

        return redirect("/performance/")
        
        #  SAVE ALL SUMMARY SCORES
    if request.method == "POST" and "save_all" in request.POST:

        for key, value in request.POST.items():
            if key.startswith("score_") and value.strip():
                emp_id = key.split("_")[1]

                if value:
                    emp = UsersData.objects.get(pk=emp_id)

                    Performance.objects.update_or_create(
                        user=emp,
                        month=str(selected_month),
                        defaults={
                            "performance_score": int(value),
                            "employee_id": str(emp_id),
                        }
                    )

        messages.success(request, "All performance scores updated successfully.")
        return redirect("/performance/")



    return render(request , "performance.html",{"page_monthly":page_monthly , "current_month":current_month, "month":selected_month})