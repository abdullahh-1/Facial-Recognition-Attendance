import csv
import datetime
import functions


if __name__ == '__main__':
    # get students from image
    student_names = functions.digital_attendance()

    # if students are found
    if student_names:
        curr_date = datetime.date.today()
        f = open('attendance.csv', 'r')
        data = csv.reader(f)
        last_line = f.readlines()[-1]
        last_name, comma, last_date = last_line.partition(',')
        f.close()

        f = open('attendance.csv', 'a')
        writer_object = csv.writer(f)

        for name in student_names:
            if last_date == curr_date:
                if functions.search_name(name, data):  # attendance is already marked
                    exit(0)
                else:
                    new_entry = [name, curr_date]
                    writer_object.writerow(new_entry)
            else:
                # new date
                writer_object.writerow(curr_date)
                new_entry = [name, curr_date]
                writer_object.writerow(new_entry)

        f.close()
