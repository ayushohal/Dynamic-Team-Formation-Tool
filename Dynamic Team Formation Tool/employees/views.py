# employees/views.py
from django.shortcuts import render, redirect
from .forms import EmployeeForm  # Ensure this import points to your EmployeeForm
from django.http import HttpResponse
from .models import Employee  # Ensure your Employee model is imported
import numpy as np
from collections import defaultdict

from scipy.optimize import linear_sum_assignment

def home(request):
    return render(request, 'home.html')  # Rendering the home template

def register_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')  # Redirect to the success page after registration
    else:
        form = EmployeeForm()
    return render(request, 'register.html', {'form': form})

def success(request):
    return render(request, 'success.html')  # Render a success page after registration


def employee_list(request):
    employees = Employee.objects.all()  # Fetch all employee records
    return render(request, 'employee_list.html', {'employees': employees})  # Pass the data to the template


def form_teams(request):
    teams = defaultdict(list)
    error_message = None

    if request.method == 'POST':
        team_size = int(request.POST.get('team_size'))
        skills_required = set(request.POST.get('skills').split(','))

        # Fetch employees from the database
        employees = Employee.objects.all()

        # Prepare lists and structures for the bipartite graph
        valid_employees_by_skill = {skill: [] for skill in skills_required}
        employee_list = []

        # Collect employees with their skills
        for employee in employees:
            employee_skills = set(employee.skills.split(','))
            employee_list.append(employee)
            for skill in skills_required.intersection(employee_skills):
                valid_employees_by_skill[skill].append(employee)

        # Create a cost matrix for the Hungarian algorithm
        num_skills = len(skills_required) * team_size
        num_employees = len(employee_list)
        cost_matrix = np.ones((num_skills, num_employees))  # Start with all 1s

        skill_index = {skill: idx for idx, skill in enumerate(skills_required)}

        # Fill the cost matrix
        for skill, employees in valid_employees_by_skill.items():
            for i in range(team_size):
                if i < num_skills:  # Ensure we don't exceed the skill slots
                    for employee in employees:
                        emp_index = employee_list.index(employee)
                        cost_matrix[skill_index[skill] * team_size + i, emp_index] = 0  # Assign 0 cost if employee has the skill

        # Apply the Hungarian algorithm to find the optimal assignment
        row_ind, col_ind = linear_sum_assignment(cost_matrix)

        # Create a mapping of employees to skills
        skill_to_teams = defaultdict(list)
        assigned_employees = set()  # Track assigned employees

        for row, col in zip(row_ind, col_ind):
            # Calculate which skill and which slot this corresponds to
            skill_slot_index = row // team_size
            if row < num_skills and col < num_employees and cost_matrix[row, col] == 0:
                skill = list(skills_required)[skill_slot_index]
                employee = employee_list[col]
                if employee not in assigned_employees:  # Check if employee is already assigned
                    skill_to_teams[skill].append(employee)
                    assigned_employees.add(employee)  # Mark employee as assigned

        # Collect teams based on assigned employees
        for skill in skills_required:
            if len(skill_to_teams[skill]) < team_size:
                error_message = f"Not enough employees with {skill} skill to complete the team size. Only {len(skill_to_teams[skill])} members assigned."
            for employee in skill_to_teams[skill]:
                teams[skill].append(f"{employee.name} ({employee.skills})")


            # If no employees were assigned to a skill, add a custom message
            if not teams[skill]:
                teams[skill].append("No employees available with this skill.")

    return render(request, 'form_teams.html', {'teams': dict(teams), 'error_message': error_message})











