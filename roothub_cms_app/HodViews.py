from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.utils.timezone import now
from datetime import datetime
from .models import Admin, Attendance, AttendanceReport, Courses, CustomUser, Trainee, Trainers


def admin_home(request):
    admin = Admin.objects.all()
    return render(request,"hod_template/home_content.html", {"admin":admin})

def add_trainer(request):
    return render(request,"hod_template/add_trainer_template.html")

def add_trainer_save(request):
    if request.method != "POST":
        return HttpResponseRedirect("error_404")
    
    
    first_name = request.POST.get("first_name").capitalize()
    middle_name = request.POST.get("middle_name").capitalize()
    last_name = request.POST.get("last_name").capitalize()
    email = request.POST.get("email").lower().replace(' ', '')
    password = request.POST.get("password")
    username = request.POST.get("username")
    gender = request.POST.get("gender")
    profile_pic = request.FILES.get('profile_pic')
    address = request.POST.get("address")
    religion = request.POST.get("religion")
    state = request.POST.get("state")
    country = request.POST.get("country")
    phone  = request.POST.get("number")

    try:
        if profile_pic:
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name,profile_pic)
            profile_pic_url = fs.url(filename)
        else:
            profile_pic_url= None

        # if profile_pic_url:
        #     user.profile_pic = profile_pic_url  # Save the URL if available
        # else:
        #     user.profile_pic = '/static/balnk.webp'

        try:
            # Check if the email already exists
            if CustomUser.objects.filter(email__iexact=email).exists():
                messages.error(request, "Email already exists!")
                return render(request, 'hod_template/add_trainer_template.html', {'data': request.POST})

            # Check if the username already exists
            elif CustomUser.objects.filter(username__iexact=username).exists():
                messages.error(request, "Username already exists!")
                return render(request, 'hod_template/add_trainer_template.html', {'data': request.POST})
            
            # Validate required fields
            elif not first_name or not last_name or not username or not gender:
                messages.error(request, "Please fill all the required fields.")
                return render(request, 'hod_template/add_trainer_template.html', {'data': request.POST})
            
            elif not password:
                messages.error(request, "Password must not be empty.")
            elif len(password) < 8:
                messages.error(request, "Password must be at least 8 characters long.")

            elif 11>len(phone)>15:
                messages.error(request,"Input an appropiate phone number")
            
            else:
                # Create the CustomUser instance
                user = CustomUser.objects.create_user(
                    first_name=first_name,
                    middle_name=middle_name,
                    last_name=last_name,
                    email=email,
                    password=password,
                    username=username,
                    profile_pic=profile_pic_url,
                    user_type=2
                )
                user.save()
                
                trainer = user.trainers 
                trainer.gender = gender
                trainer.address = address
                trainer.religion = religion
                trainer.state = state
                trainer.country = country
                trainer.phone = phone
                trainer.save()

                messages.success(request, "Staff Added Successfully")
                return HttpResponseRedirect("admin_home")

        except Exception as e:
            print(e)
            messages.error(request, "An unexpected error occurred")
            return HttpResponseRedirect("add_trainer")
    except Exception as p:
        print(p)
        messages.error(request, "An unexpected error occurred")
        return HttpResponseRedirect("add_trainer")

def add_course(request):
    return render(request,"hod_template/add_course.html")

def add_courses_save(request):
    if request.method == "POST":
        course_name = request.POST.get("course_name") 
        price = request.POST.get('price', "").strip() 

        # Check for empty input
        if not course_name:
            messages.error(request, "Course name cannot be empty.")

        if not price:
            messages.error(request, "Price cannot be empty.")

        try:
            price_value = float(price)
            if price_value <= 0:
                messages.error(request, "Price must be a positive number.")

        except ValueError:
            messages.error(request, "Price must be a valid number.")

        
        # # Check for invalid characters
        # elif not course_name.replace(" ", "").isalnum():
        #     messages.error(request, "Course name must contain only letters, numbers, and spaces.")
        
        # Check for excessively long input
        if len(course_name) > 255:
            messages.error(request, "Course name is too long. Maximum length is 255 characters.")
        
        # Check for duplicates (case-insensitive)
        elif Courses.objects.filter(course_name__iexact=course_name).exists():
            messages.error(request, f"The course '{course_name}' already exists.")
    
            # Save the course to the database
        else:
            try:
                new_course = Courses.objects.create(course_name=course_name , price_name=price_value)
                new_course.save()
                messages.success(request, f"The Course: '{course_name}' has been added successfully with its corresponding price '{price}'!")
                return HttpResponseRedirect("admin_home") 
            
            # except Courses.DoesNotExist:
            #     messages.error(request, "The selected course does not exist.")
            except Exception as e:
                    # Catch any unexpected database or system errors
                    print(e)
                    messages.error(request, f"An error occurred while adding the course and price")

    else:
        # Handle invalid methods (GET, DELETE, etc.)
        messages.error(request, "Invalid action. Use the form to submit a price.")

    return render(request,"hod_template/add_course.html")

def add_trainee(request):
    trainee = Trainee.objects.all()
    courses = Courses.objects.all()
    return render(request,"hod_template/add_trainee_template.html", {"trainee": trainee,"courses":courses})

def add_trainee_save(request):
    if request.method != "POST":
        return HttpResponseRedirect("error_404")
    
    
    first_name = request.POST.get("first_name").capitalize()
    middle_name = request.POST.get("middle_name").capitalize()
    last_name = request.POST.get("last_name").capitalize()
    email = request.POST.get("email").lower().replace(' ', '')
    password = request.POST.get("password")
    username = request.POST.get("username")
    gender = request.POST.get("gender")
    profile_pic = request.FILES.get('profile_pic')
    address = request.POST.get("address")
    religion = request.POST.get("religion")
    state = request.POST.get("state")
    country = request.POST.get("country")
    phone  = request.POST.get("number")
    course_choice = request.POST.get("course")

    try:
        if profile_pic:
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name,profile_pic)
            profile_pic_url = fs.url(filename)
        else:
            profile_pic_url= None

        try:
            # Check if the email already exists
            if CustomUser.objects.filter(email__iexact=email).exists():
                messages.error(request, "Email already exists!")
                return render(request, 'hod_template/add_trainer_template.html', {'data': request.POST})

            # Check if the username already exists
            elif CustomUser.objects.filter(username__iexact=username).exists():
                messages.error(request, "Username already exists!")
                return render(request, 'hod_template/add_trainer_template.html', {'data': request.POST})
            
            # Validate required fields
            elif not first_name or not last_name or not username or not gender:
                messages.error(request, "Please fill all the required fields.")
                return render(request, 'hod_template/add_trainer_template.html', {'data': request.POST})
            
            elif not password:
                messages.error(request, "Password must not be empty.")
            elif len(password) < 8:
                messages.error(request, "Password must be at least 8 characters long.")

            elif 11>len(phone)>15:
                messages.error(request,"Input an appropiate phone number")
            
            else:
                user = CustomUser.objects.create_user(
                    first_name=first_name,
                    middle_name=middle_name,
                    last_name=last_name,
                    email=email,
                    password=password,
                    username=username,
                    profile_pic=profile_pic_url,
                    user_type=3
                )
                
                trainees = user.trainee
                trainees.gender = gender
                trainees.address = address
                trainees.religion = religion
                trainees.state = state
                trainees.country = country
                trainees.phone = phone

                selected_course = Courses.objects.get(id=course_choice)
                trainees.course_id = selected_course 
                trainees.save()
                user.save()

                messages.success(request, "Trainer Added Successfully")
                return HttpResponseRedirect("admin_home")

        except Exception as e:
            print(e)
            messages.error(request, "An unexpected error occurred")
            return HttpResponseRedirect("add_trainee")
    except Exception as p:
        print(p)
        messages.error(request, "An unexpected error occurred")
        return HttpResponseRedirect("add_trainee")

def view_trainer(request):
    trainers = Trainers.objects.all()
    pics = CustomUser.objects.all()
    return render(request,"hod_template/view_trainer.html" ,{"trainers": trainers,"pics":pics})

def view_course(request):
    courses = Courses.objects.all()
    return render(request,"hod_template/view_course.html" ,{"courses": courses})

def view_trainee(request):
    trainees = Trainee.objects.all()
    course = Courses.objects.all()
    return render(request,"hod_template/view_trainee.html" ,{"trainees": trainees,"course":course})

def edit_trainer(request, trainer_id):
    try:
        trainers = get_object_or_404(Trainers, admin=trainer_id)
        return render(request, "hod_template/edit_trainer.html", {"trainers": trainers})
    except Trainers.DoesNotExist:
        messages.error(request, "Trainer not found!")
        return HttpResponseRedirect("error_404")
    
def edit_trainer_save(request, trainer_id):
    if request.method != "POST":
        return HttpResponseRedirect("error_404")

    users = get_object_or_404(CustomUser, id=trainer_id)
    trainers = get_object_or_404(Trainers, admin=users)
    
    
    first_name = request.POST.get("first_name", "").capitalize()
    middle_name = request.POST.get("middle_name", "").capitalize()
    last_name = request.POST.get("last_name", "").capitalize()
    email = request.POST.get("email", "").lower().strip()
    password = request.POST.get("password", "")
    username = request.POST.get("username", "").strip()
    gender = request.POST.get("gender", "")
    profile_pic = request.FILES.get('profile_pic')
    address = request.POST.get("address", "")
    religion = request.POST.get("religion", "")
    state = request.POST.get("state", "")
    country = request.POST.get("country", "")
    phone = request.POST.get("number", "").strip()

    if profile_pic:
        fs = FileSystemStorage()
        filename = fs.save(profile_pic.name,profile_pic)
        profile_pic_url = fs.url(filename)
    else:
        profile_pic_url = None

    try:
        if username != users.username:
            if CustomUser.objects.filter(username__iexact=username).exclude(id=users.id).exists():
                    messages.error(request, "Username already exists!")
                    return HttpResponseRedirect(f"/edit_trainer/{trainer_id}")

        if email != users.email:
            if email == "":
                    messages.error(request, "Email cannot be empty!")
                    return HttpResponseRedirect(f"edit_trainer/{trainer_id}")
            elif CustomUser.objects.filter(email__iexact=email).exclude(id=users.id).exists():
                    messages.error(request, "Email already exists!")
                    return HttpResponseRedirect(f"/edit_trainer/{trainer_id}")

        if not phone.isdigit() or not (11 <= len(phone) <= 15):
                messages.error(request, "Phone number must be between 11 and 15 digits!")
                return HttpResponseRedirect(f"/edit_trainer/{trainer_id}")
            

        users.first_name = first_name
        users.middle_name = middle_name
        users.last_name = last_name
        users.email = email
        if password:
            users.set_password(password)
        users.username = username
        if profile_pic:
            users.profile_pic = profile_pic_url
        else:
            users.profile_pic = users.profile_pic
        trainers.gender = gender
        trainers.address = address
        trainers.religion = religion
        trainers.state = state
        trainers.country = country
        trainers.phone = phone
        users.save()
        trainers.save()

        messages.success(request, "Trainer updated successfully!")
        return HttpResponseRedirect("/admin_home")
    except Exception as e:
                print(e)
                messages.error(request, "Failed to edit staff")
                return HttpResponseRedirect(f"/edit_trainer/{trainer_id}")
    

def edit_trainee(request, trainee_id):
    try:
        trainees = get_object_or_404(Trainee, admin=trainee_id)
        courses = Courses.objects.all()
        return render(request, "hod_template/edit_trainee.html", {"trainees": trainees, "courses": courses})
    except Trainers.DoesNotExist:
        messages.error(request, "Trainee not found!")
        return HttpResponseRedirect("error_404")
    
def edit_trainee_save(request, trainee_id):
    if request.method != "POST":
        return HttpResponseRedirect("error_404")

    users = get_object_or_404(CustomUser, id=trainee_id)
    trainees = get_object_or_404(Trainee, admin=users)
    
    
    first_name = request.POST.get("first_name", "").capitalize()
    middle_name = request.POST.get("middle_name", "").capitalize()
    last_name = request.POST.get("last_name", "").capitalize()
    email = request.POST.get("email", "").lower().strip()
    password = request.POST.get("password", "")
    username = request.POST.get("username", "").strip()
    gender = request.POST.get("gender", "")
    profile_pic = request.FILES.get('profile_pic')
    address = request.POST.get("address", "")
    religion = request.POST.get("religion", "")
    state = request.POST.get("state", "")
    country = request.POST.get("country", "")
    phone = request.POST.get("number", "").strip()
    course_choice = request.POST.get("course")

    if profile_pic:
        fs = FileSystemStorage()
        filename = fs.save(profile_pic.name,profile_pic)
        profile_pic_url = fs.url(filename)
    else:
        profile_pic_url = users.profile_pic

    try:


        if username != users.username:
            if CustomUser.objects.filter(username__iexact=username).exclude(id=users.id).exists():
                    messages.error(request, "Username already exists!")
                    return HttpResponseRedirect(f"/edit_trainee/{trainee_id}")

        if email != users.email:
            if email == "":
                    messages.error(request, "Email cannot be empty!")
                    return HttpResponseRedirect(f"edit_trainee/{trainee_id}")
            elif CustomUser.objects.filter(email__iexact=email).exclude(id=users.id).exists():
                    messages.error(request, "Email already exists!")
                    return HttpResponseRedirect(f"/edit_trainee/{trainee_id}")

        if not phone.isdigit() or not (11 <= len(phone) <= 15):
                messages.error(request, "Phone number must be between 11 and 15 digits!")
                return HttpResponseRedirect(f"/edit_trainee/{trainee_id}")
            

        users.first_name = first_name
        users.middle_name = middle_name
        users.last_name = last_name
        users.email = email
        if password:
            users.set_password(password)  
        users.username = username
        if profile_pic:
            users.profile_pic = profile_pic_url
        else:
            users.profile_pic = users.profile_pic
        trainees.gender = gender
        trainees.address = address
        trainees.religion = religion
        trainees.state = state
        trainees.country = country
        trainees.phone = phone

        if course_choice:
            selected_course = Courses.objects.get(id=course_choice)
            trainees.course_id = selected_course  
        trainees.save()
        users.save()

        messages.success(request, "Trainee updated successfully!")
        return HttpResponseRedirect("/admin_home")
    except Exception as e:
                print(e)
                messages.error(request, "Failed to edit Trainee")
                return HttpResponseRedirect(f"/edit_trainee/{trainee_id}")
        
def edit_course(request,course_id):
    try:
        courses = get_object_or_404(Courses, id=course_id)
        return render(request, "hod_template/edit_course.html", {"courses": courses})
    except Trainers.DoesNotExist:
        messages.error(request, "Course not found!")
        return HttpResponseRedirect("error_404")

def edit_course_save(request,course_id):
    if request.method != "POST":
        return HttpResponseRedirect("error_404")
    
    else:
        courses = get_object_or_404(Courses, id=course_id)

        course_name = request.POST.get("course_name")
        price = request.POST.get("price")

        if not course_name:
            messages.error(request, "Course name cannot be empty.")

        if not price:
            messages.error(request, "Price cannot be empty.")

        try:
            
            if course_name != courses.course_name:
                if CustomUser.objects.filter(course_name__iexact=course_name).exclude(id=courses.id).exists():
                    messages.error(request, "Course already exists!")
                    return HttpResponseRedirect(f"edit_trainer/{course_id}")
            
            courses.course_name = course_name
            courses.price_name = price
            courses.save()

            messages.success(request, f"The course'{courses.course_name}'has been successfully update to '{course_name}' with the price '{price}'")
            return HttpResponseRedirect("/admin_home")

        except ValueError:
            messages.error(request, "Price must be a valid number.")
            return HttpResponseRedirect(f"/edit_course/{course_id}")
        except Exception as e:
            print(e)
            messages.error(request, "An unexpected error occured!")
            return HttpResponseRedirect(f"/edit_course/{course_id}")


def assign_trainer(request):
    courses = Courses.objects.all()
    trainers = Trainers.objects.all()

    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        trainer_id = request.POST.get('trainer_id')

        course = get_object_or_404(Courses, id=course_id)
        trainer = get_object_or_404(Trainers, id=trainer_id)

        if course.trainer_id:
            confirmation = request.POST.get('confirmation', 'no')
            if confirmation == 'yes':
                current_trainer = course.trainer_id
                course.trainer_id = trainer
                course.save()
                trainer.course_id.add(course)
                current_trainer.course_id.remove(course)

                messages.success(request, f" The Trainer '{trainer.admin.first_name} {trainer.admin.last_name}' has been assigned to the course {course.course_name}.")
            else:
                messages.info(request, "Trainer assignment was cancelled.")
        else:
            course.trainer_id = trainer
            course.save()
            trainer.course_id.add(course)

            messages.success(request, f" The Trainer '{trainer.admin.first_name} {trainer.admin.last_name}' has been assigned to the course {course.course_name}.")

        return HttpResponseRedirect('assign_trainer')

    return render(request, 'hod_template/assign_trainer.html', {'courses': courses, 'trainers': trainers})

def get_current_trainer(request, course_id):
    course = get_object_or_404(Courses, id=course_id)
    if course.trainer_id:
        trainer_name = f"{course.trainer_id.admin.first_name} {course.trainer_id.admin.last_name}"
    else:
        trainer_name = None
    return JsonResponse({'trainer': trainer_name})

def delete_trainer(request,trainer_id):
    pass

def delete_trainee(request,trainee_id):
    pass

def mark_attendance(request):
    courses = Courses.objects.all()

    if request.method == "POST":
        course_id = request.POST.get("course_id")
        date = request.POST.get("date")

        if not course_id or not date:
            return render(request, "hod_template/mark_attendance.html", {
                "courses": courses,
                "error": "Please select a course and date."
            })

        try:
            date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            return render(request, "hod_template/mark_attendance.html", {
                "courses": courses,
                "error": "Invalid date format. Please select a valid date."
            })

        # Get course and create attendance record
        course = get_object_or_404(Courses, id=course_id)
        attendance, created = Attendance.objects.get_or_create(
            course=course, attendance_date=date
        )

        # Mark trainees' attendance
        present_ids = request.POST.getlist("present")  # IDs of trainees marked as Present
        absent_ids = request.POST.getlist("absent")  # IDs of trainees marked as Absent

        # Process Present trainees
        for trainee_id in present_ids:
            trainee = get_object_or_404(Trainee, id=trainee_id)
            AttendanceReport.objects.update_or_create(
                attendance_id=attendance,
                student_id=trainee,
                status=True  # Mark as Present
            )

        # Process Absent trainees
        for trainee_id in absent_ids:
            trainee = get_object_or_404(Trainee, id=trainee_id)
            AttendanceReport.objects.update_or_create(
                attendance_id=attendance,
                student_id=trainee,
                status=False # Mark as Absent
            )
        messages.success(request,"Attendance marked sucessfully")
        return HttpResponseRedirect("view_attendance")

    return render(request, "hod_template/mark_attendance.html", {
        "courses": courses
    })


def get_trainees(request):
    course_id = request.GET.get("course_id")
    date = request.GET.get("date")

    try:
        course = Courses.objects.get(id=course_id)
        trainees = course.trainees.all()
        if not trainees.exists():
            return JsonResponse({"error": "No students found for this course"}, status=404)

        trainee_data = [
            {"id": trainee.id, "name": f"{trainee.admin.first_name} {trainee.admin.last_name}"}
            for trainee in trainees
        ]
        return JsonResponse({"trainees": trainee_data}, status=200)

    except Courses.DoesNotExist:
        return JsonResponse({"error": "Course not found"}, status=404)
    except Exception as e:
        print(e)
        return JsonResponse({"error": "An unexpected error occurred"}, status=500)


def view_attendance(request):
    courses= Courses.objects.all()
    return render(request, "hod_template/view_attendance.html",{"courses":courses})

def get_students(request):
    course_id = request.GET.get("course_id")
    try:
        course = Courses.objects.get(id=course_id)
        
        trainees = course.trainees.all()

        if not trainees.exists():
            return JsonResponse({"error": "No students found for this course"}, status=404)

        student_data = [
            {
                "id": trainee.id,
                "name": f"{trainee.admin.first_name} {trainee.admin.last_name}"
            }
            for trainee in trainees
        ]
        return JsonResponse({"students": student_data}, status=200)

    except Courses.DoesNotExist:
        return JsonResponse({"error": "Course not found"}, status=404)
    except Exception as e:
        print(e)
        return JsonResponse({"error": "An unexpected error occurred"}, status=500)


def get_attendance_data(request, trainee_id):
    try:
        # Get the trainee and their registration date
        trainee = Trainee.objects.get(id=trainee_id)
        registration_date = trainee.created_at.date()  # Registration date
    except Trainee.DoesNotExist:
        return JsonResponse({"error": "Trainee not found"}, status=404)

    # Fetch attendance records
    attendance_records = AttendanceReport.objects.filter(
        student_id=trainee_id, 
        attendance_id__attendance_date__gte=registration_date
    ).select_related('attendance_id')

    if not attendance_records.exists():
        return JsonResponse({
            "trainee_name": f"{trainee.admin.first_name} {trainee.admin.last_name}",
            "dates": [],
            "status": [],
            "present_percentage": 0,
            "absent_percentage": 0,
            "message": "No attendance records found for this trainee."
        })

    # Prepare data
    result_dates = []
    result_status = []
    present_count = 0
    absent_count = 0

    for record in attendance_records:
        attendance_date = record.attendance_id.attendance_date
        status = record.status
        result_dates.append(attendance_date.strftime("%Y-%m-%d"))
        result_status.append(status)
        if status:
            present_count += 1
        else:
            absent_count += 1

    # Calculate percentages
    total_marked = present_count + absent_count
    present_percentage = round((present_count / total_marked) * 100, 2) if total_marked > 0 else 0
    absent_percentage = round((absent_count / total_marked) * 100, 2) if total_marked > 0 else 0

    # Return data
    return JsonResponse({
        "trainee_name": f"{trainee.admin.first_name} {trainee.admin.last_name}",
        "dates": result_dates,
        "status": result_status,
        "present_percentage": present_percentage,
        "absent_percentage": absent_percentage,
    })


def mark_presentation(request):
    courses = Courses.objects.all()
    return render(request,"hod_template/mark_presentation.html",{"courses":courses})