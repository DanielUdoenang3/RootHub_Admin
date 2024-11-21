from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages

from roothub_cms_app.models import Courses, CustomUser, Prices


def admin_home(request):
    return render(request,"hod_template/home_content.html")

def add_staff(request):
    return render(request,"hod_template/add_staff_template.html")

def add_staff_save(request):
    if request.method !="POST":
        return HttpResponseRedirect("error_404")
    else:
        first_name = request.POST.get("first_name").capitalize()
        middle_name = request.POST.get("middle_name").capitalize()
        last_name = request.POST.get("last_name").capitalize()
        email = request.POST.get("email").lower().replace(' ', '')
        password = request.POST.get("password")
        username = request.POST.get("username").lower().replace(' ', '')
        gender = request.POST.get("gender")
        address = request.POST.get("address")
        religion = request.POST.get("religion")
        state = request.POST.get("state")
        country = request.POST.get("country")
        try:
            user = CustomUser.objects.create_user(
                first_name = first_name,
                middle_name = middle_name,
                last_name =last_name,
                email =email,
                password =password,
                username=username,
                gender =gender,
                address =address,
                religion =religion,
                state =state,
                country =country
            )
            user.save()
            messages.success(request, "Staff Added Successfully")
            return HttpResponseRedirect("add_staff")
        except:
            messages.error(request, "An unexpected error occured")
            return HttpResponseRedirect("add_staff")

def add_course(request):
    return render(request,"hod_template/add_course.html")

def add_courses_save(request):
    if request.method == "POST":
        course_name = request.POST.get("course_name")  

        # Check for empty input
        if not course_name:
            messages.error(request, "Course name cannot be empty.")
        
        # # Check for invalid characters
        # elif not course_name.replace(" ", "").isalnum():
        #     messages.error(request, "Course name must contain only letters, numbers, and spaces.")
        
        # Check for excessively long input
        elif len(course_name) > 255:
            messages.error(request, "Course name is too long. Maximum length is 255 characters.")
        
        # Check for duplicates (case-insensitive)
        elif Courses.objects.filter(course_name__iexact=course_name).exists():
            messages.error(request, f"The course '{course_name}' already exists.")
        
        else:
            # Save the course to the database
            try:
                new_course = Courses.objects.create(course_name=course_name)
                new_course.save()  # Save explicitly if needed, but `create` handles this
                messages.success(request, f"The Course: '{course_name}' has been added successfully!")
                return HttpResponseRedirect("add_price")  # Refresh the page after success
            except Exception as e:
                # Catch any unexpected database or system errors
                messages.error(request, f"An error occurred while adding the course: {str(e)}")

    return render(request,"hod_template/add_course.html")

def add_price(request):
    # Render available courses for GET requests
    courses = Courses.objects.all()
    return render(request,"hod_template/add_price.html", {"courses": courses})

def add_price_save(request):
    if request.method == "POST":
        course_id = request.POST.get('course')
        price = request.POST.get('price', "").strip()

        # Check for empty price
        if not price:
            messages.error(request, "Price cannot be empty.")
            return HttpResponseRedirect("add_price")  # Correct the redirect URL

        # Validate price format
        try:
            price_value = float(price)
            if price_value <= 0:
                messages.error(request, "Price must be a positive number.")
                return HttpResponseRedirect("add_price")
        except ValueError:
            messages.error(request, "Price must be a valid number.")
            return HttpResponseRedirect("add_price")

        # Validate course selection
        if not course_id:
            messages.error(request, "Please select a course.")
            return HttpResponseRedirect("add_price")

        # Save price to database
        try:
            course = Courses.objects.get(id=course_id)
            Prices.objects.create(price_name=price_value, course=course)
            messages.success(request, f"Price '{price_value}' added successfully for course '{course.course_name}'.")
            return HttpResponseRedirect("admin_home")  # Redirect to admin home after success
        except Courses.DoesNotExist:
            messages.error(request, "The selected course does not exist.")
            return HttpResponseRedirect("add_price")
        except Exception as e:
            print(f"Error creating price: {e}")
            messages.error(request, "An unexpected error occurred while adding the price. Please try again.")
            return HttpResponseRedirect("add_price")

    else:
        # Handle invalid methods (GET, DELETE, etc.)
        messages.error(request, "Invalid action. Use the form to submit a price.")
        return HttpResponseRedirect("add_price")

    # Render available courses for GET requests
        

