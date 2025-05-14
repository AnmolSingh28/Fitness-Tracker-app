# views.py
from django.shortcuts import render, redirect
from tracker.models import Workout, Exercise
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from datetime import timedelta

@login_required

def add_workout(request):
    if request.method == 'POST':
        try:
            # Get workout name from form
            workout_name = request.POST['name']
            workout = Workout.objects.create(name=workout_name)

            # Get exercise details from form
            exercise_names = request.POST.getlist('exercise_name')
            reps_list = request.POST.getlist('reps')
            weight_list = request.POST.getlist('weight')
            duration_list = request.POST.getlist('duration')

            # Save exercises for the workout
            for i in range(len(exercise_names)):
                Exercise.objects.create(
                    workout=workout,
                    name=exercise_names[i],
                    reps=reps_list[i],
                    weight=weight_list[i],
                    duration=duration_list[i]
                )

            return redirect('logbook')  # or wherever you want to redirect after submission

        except Exception as e:
            return render(request, 'tracker/add_workout.html', {
                'error': f"An error occurred: {str(e)}"
            })

    return render(request, 'tracker/add_workout.html')

def user_login(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        
        if user is not None:
            login(request,user)
            return redirect("dash_board")
        else:
            return render(request,'tracker/login.html',{'error':'Invalid username or password'})
    return render(request,'tracker/login.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. You can now log in.')
            return redirect('user_login') 
    else:
        form = UserCreationForm()
    return render(request, 'tracker/register.html', {'form': form})

@login_required
def workout_detail(request, workout_id):
    workout = get_object_or_404(Workout, id=workout_id)
    print(workout.exercises.all())
    return render(request, 'tracker/workout_detail2.html', {'workout': workout})

    return render(request, 'tracker/workout_detail.html', {'workout': workout1, 'exercises': exercises})
def dash_board(request):
    return render(request, 'tracker/dashboard.html')

@login_required
def home(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    return render(request,'tracker/home.html')
def logbook(request):
    #workouts = Workout.objects.all().order_by('-created_at')
    #workouts = Workout.objects.all().prefetch_related('exercises')
    workouts = Workout.objects.all().filter(user=request.user).prefetch_related('exercises').order_by('-created_at')
    #exercises = Exercise.objects.all()
    return render(request, 'tracker/logbook.html', {'workouts': workouts})#'exercises':exercises})

def time_to_seconds(time_str):
    try:
        h, m, s = map(int, time_str.strip().split(":"))
        return int(timedelta(hours=h, minutes=m, seconds=s).total_seconds())
    except:
        return 0
    
@login_required
def save_workout(request):
    if request.method == 'POST':
        workout_name = request.POST.get('name')
        exercises_data = zip(
            request.POST.getlist('exercise_name[]'),
            request.POST.getlist('reps[]'),
            request.POST.getlist('weight[]'),
            request.POST.getlist('duration[]')
        )
        

        if not workout_name:
            return render(request, 'tracker/add_workout.html', {'error': 'Workout name is required'})

        workout = Workout.objects.create(user=request.user, name=workout_name, created_at=timezone.now())

        for name, reps, weight, duration in exercises_data:
            
            if name.strip():
                Exercise.objects.create(
                    workout=workout,
                    exercise_name=name,
                    reps=reps,
                    weight=weight,
                    duration=time_to_seconds(duration)
                )
        #exercises = workout.exercises.all()
       # for ex in exercises:
       
        #    ex.formatted_duration = format_duration(ex.duration)

        request.session['workout_saved'] = True
        
        workout_saved = request.session.pop('workout_saved', False)
        return render(request, 'tracker/workout_saved.html', {
            'workout': workout,
            'exercises': workout.exercises.all()
        })

    return render(request, 'tracker/add_workout.html',{'workout_saved': workout_saved})
