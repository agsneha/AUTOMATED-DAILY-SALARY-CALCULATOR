"""
Sneha Agrawal
CLASS: CS 521- Fall 2023
DATE: 13-DECEMBER-2023
FINAL PROJECT, Automated daily salary calculator.
"""

import datetime


class Employee:
    def __init__(self, emp_id, emp_name, base_salary_per_hour):
        """
        Initialize Employee object with employee ID, name and base salary per hour.
        """
        try:
            # Private Attribute
            self.__base_salary_per_hour = float(base_salary_per_hour)
            # Public Attributes
            self.emp_id = int(emp_id)
            self.emp_name = emp_name
            # Container (list) for attendance records
            self.attendance = []
        except ValueError as error_in_init:
            raise ValueError("Invalid. EmployeeID should be an integer, and base salary a float.") from error_in_init

    def get_emp_id(self):
        """
        Get the employee ID.
        """
        return self.emp_id

    def get_base_salary_per_hour(self):
        """
        Get the base salary per hour.
        """
        return self.__base_salary_per_hour

    def punch_in(self, time_str):
        """
        Record employee's punch-in time.
        """
        try:
            time_in = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M")
            self.attendance.append({"Status": "IN", "Punch In Time": time_in})
        except ValueError as punch_in_error:
            raise ValueError("Invalid time format. Please use YYYY-MM-DD HH:MM format for punch in time.") \
                from punch_in_error

    def punch_out(self, time_str):
        """
            Record employee's punch-out time.
        """
        try:
            time_out = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M")
            self.attendance.append({"Status": "OUT", "Punch Out Time": time_out})
        except ValueError as punch_out_error:
            raise ValueError("Invalid time format. Please use YYYY-MM-DD HH:MM format for punch out time.") \
                from punch_out_error

    def apply_leave(self, start_time_string, end_time_string):
        """
        Record employee's leave application.
        """
        try:
            start_time = datetime.datetime.strptime(start_time_string, "%H:%M")
            end_time = datetime.datetime.strptime(end_time_string, "%H:%M")
            self.attendance.append({"Start_Time": start_time, "End_Time": end_time, "Status": "LEAVE"})
        except ValueError as apply_leave_error:
            raise ValueError("Invalid time format. Please use YYYY-MM-DD HH:MM.") from apply_leave_error

    def __calculate_daily_salary(self):
        """
        Calculate employee's daily salary based on attendance records and salary rules.
        """
        daily_salary = 0
        punch_in_time = None
        duration = 0  # Local variable for duration
        # Standard work hours per day by policy
        standard_work_hour = 9

        for entry in self.attendance:
            status = entry["Status"]
            punch_time_in = entry.get("Punch In Time")
            punch_time_out = entry.get("Punch Out Time")

            if status == "IN" and punch_time_in is not None:
                punch_in_time = punch_time_in
            if status == "OUT" and punch_time_out is not None:
                punch_out_time = punch_time_out
                duration = (punch_out_time - punch_in_time).total_seconds() / 3600  # Convert timedelta to hours
                daily_salary = float(daily_salary + (duration * self.__base_salary_per_hour))

                # Deduct 2% for late entry
                if punch_in_time.hour > 9:  # Assuming work starts at 9:00 am
                    daily_salary *= 0.98
                elif punch_out_time.hour < 18:  # Assuming work ends at 6pm
                    daily_salary *= 0.98

            if status == "LEAVE":
                # Deduct salary for leave period
                leave_start_time = entry.get("Start_Time")
                leave_end_time = entry.get("End_Time")
                if leave_start_time is not None and leave_end_time is not None:
                    # Deduct salary for hours on leave period. With a 5% reduction
                    leave_duration = (leave_end_time - leave_start_time).total_seconds() / 3600
                    daily_salary = (daily_salary - (leave_duration * self.__base_salary_per_hour)) * 0.95

            # Add 15% for overtime work
                if duration > standard_work_hour:
                    overtime_hours = max(duration - standard_work_hour, 0)
                    daily_salary += (overtime_hours * self.__base_salary_per_hour * 0.15)

                break    # Assuming one entry each employee

        return daily_salary

    def __repr__(self):
        """
        Return a string representation of the Employee object.
        """
        return (f"Employee ID: {self.emp_id}, Employee Name: {self.emp_name}, Base Salary per hour: "
                f"{self.__base_salary_per_hour}")


class EmployeeReader:
    def __init__(self, filename):
        self.filename = filename

    def read_employee_details(self):
        """
        Read employee data from a text file and return a list of Employee objects.
        """
        employees = []
        try:
            with open(self.filename, 'r') as file:
                lines = file.readlines()

            for line in lines:
                # Split the line into words
                words = line.split()

                if 'ID:' in words and 'Name:' in words and 'Salary:' in words:
                    # Find the position of 'ID:' 'Name:' and 'Salary:'
                    id_index = words.index('ID:')
                    name_index = words.index('Name:')
                    salary_index = words.index('Salary:')

                    # Extract emp_id, emp_name, and base_salary_per_hour
                    emp_id = int(words[id_index + 1])
                    emp_name = f"{words[name_index + 1]} {words[name_index + 2]}"
                    base_salary_per_hour = float(words[salary_index + 1])

                    # No negative values for ID and salary
                    if emp_id < 0 or base_salary_per_hour < 0:
                        raise ValueError("Invalid input. Employee ID and base salary per hour should be non-negative.")

                    employees.append(Employee(emp_id, emp_name, base_salary_per_hour))

        except FileNotFoundError:
            print(f"Error: File '{self.filename}' not found.")
        except ValueError as value_error_file:
            print(f"Error: {value_error_file}")
        except Exception as cant_open:
            print(f"Error: {cant_open}")

        return employees


if __name__ == "__main__":
    file_name = "/Users/snehaagrawal/Documents/Python/Project/PyProject.txt"

    employee_reader = EmployeeReader(file_name)  # Create an instance of EmployeeReader
    employee_list = employee_reader.read_employee_details()   # Invoking read_employee_details function

    csv_output_path = "/Users/snehaagrawal/Documents/Python/Project/PyProject_Results.csv"
    try:
        # Save results to a CSV file
        with open(csv_output_path, 'w') as csvfile:
            csvfile.write("Employee ID,Employee Name,Base Salary per hour,Daily Salary\n")

            for emp in employee_list:
                while True:
                    try:
                        # Prompt user for punch-in time
                        punch_in_time_str = input(f"Enter entry time for {emp.emp_name} (YYYY-MM-DD HH:MM):")
                        emp.punch_in(punch_in_time_str)  # Record punch-in time
                        break  # Exit the loop if input is valid
                    except ValueError as input_error:
                        print(f"Error: {input_error}")

                while True:
                    try:
                        # Prompt the user for punch-out time
                        punch_out_time_str = input(f"Enter exit time for {emp.emp_name} (YYYY-MM-DD HH:MM):")
                        emp.punch_out(punch_out_time_str)  # Record punch-out time
                        break
                    except ValueError as input_error:
                        print(f"Error: {input_error}")

                while True:
                    try:
                        # Prompt user for leave start and end times
                        start_time_str = input(f"Enter leave start time for {emp.emp_name} (HH:MM, 24-hour format):")
                        end_time_str = input(f"Enter leave end time for {emp.emp_name} (HH:MM, 24-hour format):")
                        # Call the apply_leave method only if start and end times are different
                        if start_time_str != end_time_str:
                            emp.apply_leave(start_time_str, end_time_str)
                        break
                    except ValueError as input_error:
                        print(f"Error: {input_error}")

                # Invokes __repr__() method
                print(emp)

                # Print the daily salary
                print(f"Daily Salary: {emp._Employee__calculate_daily_salary()}\n")

                # Write data to the CSV file
                csvfile.write(f"{emp.emp_id},{emp.emp_name},{emp.get_base_salary_per_hour()},"
                              f"{emp._Employee__calculate_daily_salary()}\n")

            print(f"Results saved to: {csv_output_path}")

    except FileNotFoundError as file_error:
        print(f"Error: {file_error}")
    except Exception as e:
        print(f"Error: {e}")

    # Unit tests for results
    try:
        assert employee_list[0]._Employee__calculate_daily_salary() == 270.0
        assert employee_list[1]._Employee__calculate_daily_salary() == 313.6
        assert employee_list[2]._Employee__calculate_daily_salary() == 343.0
        assert employee_list[3]._Employee__calculate_daily_salary() == 495.0
        assert employee_list[4]._Employee__calculate_daily_salary() == 199.5
    except Exception as e:
        raise Exception("Unit test failed") from e


"""
INPUTS.
"""
# 1998-10-21 9:00
# 1998-10-21 18:00

# 1998-10-21 10:00
# 1998-10-21 18:00

# 1998-10-21 9:00
# 1998-10-21 16:00

# 1998-10-21 9:00
# 1998-10-21 20:00

# 1998-10-21 9:00
# 1998-10-21 18:00
# 12:00
# 14:00