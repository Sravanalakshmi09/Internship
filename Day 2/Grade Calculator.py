def get_grade(marks):
    if marks >= 90:
        return "S"
    elif marks >= 80:
        return "A"
    elif marks >= 70:
        return "B"
    elif marks >= 60:
        return "C"
    elif marks >= 50:
        return "D"
    else:
        return "F"

print("----- Grade Calculator -----")

for i in range(10):
    marks = float(input(f"Enter marks of Student {i+1} (0-100): "))
    grade = get_grade(marks)
    print(f"Student {i+1}: Grade = {grade}")