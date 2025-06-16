import csv
import os
import random  # Import the random, csv, and os modules, which are necessary for this code.


class Student:
    # Initializes the Student class with attributes: name, age, gender, grades in CS, Math, and English, behavior reference, and test score.
    def __init__(self, name, age, gender, cs_grade, math_grade, eng_grade,
                 behavior_ref, test_score):
        self.name = name  # Student's name
        self.age = age  # Student's age
        self.gender = gender  # Student's gender
        self.cs_grade = cs_grade  # Student's Computer Science grade
        self.math_grade = math_grade  # Student's Mathematics grade
        self.eng_grade = eng_grade  # Student's English grade
        self.behavior_ref = behavior_ref  # Student's behavior reference (Good/Bad)
        self.test_score = test_score  # Student's test score
        self.grade = None  # Placeholder for the calculated grade (A*, A, B, etc.)
        self.level = None  # Placeholder for the calculated level (Level 1, Level 2, etc.)

    # Calculates the student's grade and level based on their test score.
    def calculate_grade_and_level(self):
        if self.test_score >= 90:
            self.grade = 'A*'  # Grade A* for scores >= 90
        elif 80 <= self.test_score < 90:
            self.grade = 'A'  # Grade A for scores between 80 and 89
        elif 70 <= self.test_score < 80:
            self.grade = 'B'  # Grade B for scores between 70 and 79
        elif 60 <= self.test_score < 70:
            self.grade = 'C'  # Grade C for scores between 60 and 69
        else:
            self.grade = 'F'  # Grade F for scores below 60

        if self.test_score > 80:
            self.level = 'Level 1'  # Level 1 for scores > 80
        elif 60 <= self.test_score <= 80:
            self.level = 'Level 2'  # Level 2 for scores between 60 and 80
        else:
            self.level = 'Not Qualified'  # Not Qualified for scores below 60

    # Checks if the student is eligible for the course based on age, grades, behavior, and test score.
    def is_eligible(self):
        return (16 <= self.age <= 18  # Age must be between 16 and 18
                and self.cs_grade >= 6  # CS grade must be at least 6
                and self.math_grade >= 5  # Math grade must be at least 5
                and self.eng_grade >= 4  # English grade must be at least 4
                and self.behavior_ref.lower() ==
                'good'  # Behavior reference must be 'Good'
                and self.test_score >= 60  # Test score must be at least 60
                )


# Generates a list of 20 random math questions for the aptitude test.
def generate_test():
    questions = []  # Empty list to store questions
    for i in range(20):  # Loop to generate 20 questions
        num1 = random.randint(1, 10)  # Random number between 1 and 10
        num2 = random.randint(1, 10)  # Random number between 1 and 10
        operator = random.choice(['+', '-',
                                  '*'])  # Randomly choose an operator
        if operator == '+':
            answer = num1 + num2  # Addition
        elif operator == '-':
            answer = num1 - num2  # Subtraction
        elif operator == '*':
            answer = num1 * num2  # Multiplication
        questions.append((f"{num1} {operator} {num2}",
                          answer))  # Add question and answer to the list
    return questions  # Return the list of questions


# Administers the aptitude test to the student and calculates their score.
def administer_test():
    print("\n--- Aptitude Test ---")  # Print test title
    questions = generate_test()  # Generate test questions
    score = 0  # Initialize score to 0

    # Nested subroutine to handle a single question
    def ask_question(question, correct_answer, question_number):
        try:
            print(
                f"There are {20 - question_number} questions remaining. Current score: {score}/100"
            )  # Show remaining questions and current score
            user_answer = int(input(
                f"Q{question_number + 1}: {question} = "))  # Get user's answer
            if user_answer == correct_answer:  # Check if answer is correct
                print("Correct!")  # Print correct message
                return 5  # Return 5 points for correct answer
            else:
                print(f"Wrong! The correct answer was {correct_answer}."
                      )  # Print correct answer if wrong
                return 0  # Return 0 points for wrong answer
        except ValueError:  # Handle invalid input (non-integer)
            print(f"Invalid input. The correct answer was {correct_answer}.")
            return 0  # Return 0 points for invalid input

    # Loop through each question and use the nested subroutine
    for i, (question, correct_answer) in enumerate(questions):
        score += ask_question(question, correct_answer,
                              i)  # Call the nested subroutine

    print(f"\nTest Completed! Your score: {score}/100")  # Print final score
    if score > 80:
        print("You are eligible for Level 1.")  # Level 1 eligibility
    elif 60 <= score <= 80:
        print("You are eligible for Level 2.")  # Level 2 eligibility
    else:
        print("You are Not Qualified.")  # Not qualified
    return score  # Return the final score


# Saves the student's data to a CSV file.
def save_student(student):
    file_exists = os.path.isfile(
        'students.csv')  # Check if the file already exists
    with open('students.csv', 'a',
              newline='') as csvfile:  # Open the file in append mode
        fieldnames = [
            'Name', 'Age', 'Gender', 'CS Grade', 'Math Grade', 'Eng Grade',
            'Behavior', 'Test Score', 'Grade', 'Level'
        ]  # Define column names
        writer = csv.DictWriter(
            csvfile, fieldnames=fieldnames)  # Create a DictWriter object
        if not file_exists:  # Write header if the file is new
            writer.writeheader()
        writer.writerow({  # Write the student's data to the file
            'Name': student.name,
            'Age': student.age,
            'Gender': student.gender,
            'CS Grade': student.cs_grade,
            'Math Grade': student.math_grade,
            'Eng Grade': student.eng_grade,
            'Behavior': student.behavior_ref,
            'Test Score': student.test_score,
            'Grade': student.grade,
            'Level': student.level
        })


# Displays the results of all students, including their grades, levels, and eligibility.
# Recursive function to display results
def display_results(students, index=0, levels=None, gender_counts=None):
    # Initialize levels and gender_counts on the first call
    if levels is None:
        levels = {'Level 1': 0, 'Level 2': 0}
    if gender_counts is None:
        gender_counts = {
            'Level 1': {'Male': 0, 'Female': 0},
            'Level 2': {'Male': 0, 'Female': 0}
        }

    # Base case: stop recursion when all students are processed
    if index >= len(students):
        print("\n--- Summary ---")
        for level, count in levels.items():
            print(f"{level}: {count} students")
            print(f"  Males: {gender_counts[level]['Male']}, Females: {gender_counts[level]['Female']}")
        return

    # Process the current student
    student = students[index]
    eligibility = "Eligible" if student.is_eligible() else "Not Eligible"
    print(
        f"Name: {student.name}, Age: {student.age}, Gender: {student.gender}, "
        f"Grade: {student.grade}, Level: {student.level}, Eligibility: {eligibility}, Test Score: {student.test_score}"
    )

    # Update levels and gender counts
    if student.level in levels:
        levels[student.level] += 1
        gender_counts[student.level][student.gender] += 1

    # Recursive call to process the next student
    display_results(students, index + 1, levels, gender_counts)

# Main function to run the program.
if __name__ == "__main__":
    students = []  # List to store student objects
    print("--- Student Registration and Test ---")  # Print program title
    while True:  # Loop to register multiple students
        while True:  # Loop to get valid name
            __name__ = input("\nEnter student name: ").strip()  # Get student name
            if __name__:  # Check if name is not empty
                break
            print("Name cannot be empty. Please enter your name."
                  )  # Error message for empty name

        while True:  # Loop to get valid age
            age_input = input("Enter age: ").strip()  # Get student age
            if age_input.isdigit():  # Check if age is a number
                age = int(age_input)
                if 16 <= age <= 18:  # Check if age is between 16 and 18
                    break
                else:
                    print("You are not valid for this course."
                          )  # Error message for invalid age
                    exit()  # Exit program
            print("Invalid input. Please enter a valid age"
                  )  # Error message for invalid input

        while True:  # Loop to get valid gender
            gender = input("Enter gender (Male/Female): ").strip().capitalize(
            )  # Get student gender
            if gender in ['Male', 'Female']:  # Check if gender is valid
                break
            print("Invalid input. Please enter Male or Female."
                  )  # Error message for invalid gender

        while True:  # Loop to get valid CS grade
            cs_input = input(
                "Enter GCSE Computer Science grade: ").strip()  # Get CS grade
            try:
                cs_grade = int(cs_input)  # Convert input to integer
                if cs_grade <= 6 or cs_grade >= 9:  # Check if grade is valid
                    print("You are not valid for this course"
                          )  # Error message for invalid grade
                    exit()  # Exit program
                break
            except ValueError:  # Handle invalid input
                print("Invalid input. Please enter a number."
                      )  # Error message for invalid input

        while True:  # Loop to get valid Math grade
            math_input = input(
                "Enter Mathematics grade: ").strip()  # Get Math grade
            try:
                math_grade = int(math_input)  # Convert input to integer
                if math_grade <= 5 or math_grade >= 9:  # Check if grade is valid
                    print("You are not valid for this course"
                          )  # Error message for invalid grade
                    exit()  # Exit program
                break
            except ValueError:  # Handle invalid input
                print("Invalid input. Please enter a number."
                      )  # Error message for invalid input

        while True:  # Loop to get valid English grade
            eng_input = input(
                "Enter English grade: ").strip()  # Get English grade
            try:
                eng_grade = int(eng_input)  # Convert input to integer
                if eng_grade <= 4 or eng_grade >= 9:  # Check if grade is valid
                    print("You are not valid for this course"
                          )  # Error message for invalid grade
                    exit()  # Exit program
                break
            except ValueError:  # Handle invalid input
                print("Invalid input. Please enter a number."
                      )  # Error message for invalid input

        while True:  # Loop to get valid behavior reference
            behavior_ref = input("Enter behavior reference (Good/Bad): "
                                 ).strip().lower()  # Get behavior reference
            if behavior_ref in ['good',
                                'bad']:  # Check if behavior reference is valid
                break
            print("Invalid input. Please enter Good or Bad."
                  )  # Error message for invalid input

        test_score = administer_test(
        )  # Administer the aptitude test and get the score

        student = Student(name, age, gender, cs_grade, math_grade, eng_grade,
                          behavior_ref,
                          test_score)  # Create a new student object
        student.calculate_grade_and_level(
        )  # Calculate the student's grade and level
        students.append(student)  # Add the student to the list
        save_student(student)  # Save the student's data to the CSV file

        another = input("\nAdd another student? (yes/no): ").strip().lower(
        )  # Ask if the user wants to add another student
        if another != 'yes':  # Break the loop if the user says no
            break

    display_results(students)  # Display the results of all students
