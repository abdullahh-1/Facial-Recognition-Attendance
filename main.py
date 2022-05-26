import csv
import datetime
import functions


if __name__ == '__main__':
    # get students from image
    student_names = functions.digital_attendance()

    # if students are found
    if student_names:
        # reading previous data in csv
        curr_date = str(datetime.date.today())
        f = open('attendance.csv', 'r')
        reader = csv.reader(f)
        data = []
        for row in reader:
            data.extend(row)
        f.close()

        f = open('attendance.csv', 'r')
        last_line = f.readlines()[-1]
        last_name, comma, last_date = last_line.partition(',')
        if last_date == '':
            last_date = last_name
            last_name = ''
        f.close()

        last_date = last_date[:10]
        curr_date = curr_date[:10]

        f = open('attendance.csv', 'a')
        writer_object = csv.writer(f)

        for name in student_names:
            if last_date == curr_date:
                if not functions.search_name(name, data):  # attendance is already marked
                    new_entry = [name, curr_date]
                    writer_object.writerow(new_entry)
            else:
                # new date
                c_date = [curr_date]
                writer_object.writerow(c_date)
                new_entry = [name, curr_date]
                writer_object.writerow(new_entry)

        f.close()
