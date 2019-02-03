import xlsxwriter
import datetime

# Turns numbers to letters for excel column(eg. 1->A, 26->Z, 27->AA, 708->AAB)
def deciToLetters(deci):
    output = ""
    while (deci != 0):
        r = (deci -1) % 26
        deci = deci - r
        output = output + chr(r + 65)
        deci = deci // 26
    return output

# Create Excel sheet per section
def createExcelAttendance(section):
    workbook = xlsxwriter.Workbook("Excel Records/"+section+'_ARFID_Records_'+datetime.datetime.today().strftime('%b%e,%Y')+'.xlsx')
    worksheet = workbook.add_worksheet(section + ' Attendance')

    header = workbook.add_format({'bold': True, 'align':'center', 'bottom':6})
    green = workbook.add_format({'bg_color':'#ddffc6', 'bottom':3})
    red = workbook.add_format({'bg_color':'#ffccc6', 'bottom':3})
    gray = workbook.add_format({'bg_color':'#cfcfcf', 'bottom':3})
    timeCell = workbook.add_format({'num_format':0x12, 'bottom':3})
    default = workbook.add_format({'bottom':3})


    # Add headers
    labels = ["CN", "Surname", "First Name", "Middle Name", "Sex"]

    column = 0 #Letters
    for label in labels:
        worksheet.write(0, column, label, header)
        column += 1

    # Add dates in headers
    days = []   #List of days with record
    cursor.execute(queries["listDays"])
    for date in cursor:
        worksheet.write(0, column, date[0], header)
        days.append(date[0])
        column += 1


    # Classlist
    cursor.execute(queries["classList"].format(section))

    row = 1 #Starts on row 1 since row 0 holds the header
    for (classNum, surname, firstName, middleName, sex) in cursor:
        info = [classNum, surname, firstName, middleName, sex]
        j = 0
        for i in info:
            worksheet.write(row, j, i, default)
            j += 1

        # Blank info will stay blank instead of 'nan'
        while 'nan' in info:
            loc = info.index('nan')
            worksheet.write(row, loc, None, default)
            info[loc] = None
        row += 1

    # Variables about header info
    numLabels = len(labels)
    numDays = len(days)

    # List attendance per student
    cursor.execute(queries["classAttendance"].format(section))

    for (classNum, date, time) in cursor:
        col = len(labels) + days.index(date)
        worksheet.write_datetime(classNum, col, datetime.datetime.strptime(time,"%H:%M %p"), timeCell)

    rawTimeLate = "10:15"   # %H:%M
    timeLate = datetime.datetime.strptime(rawTimeLate, "%H:%M")

    # Total on time, late, absent per student #Header

    tallyLabels = ["On Time", "Lates", "Absences", "Total"]
    tallyColumn = numLabels + numDays
    for tallyLabel in tallyLabels:
        worksheet.write(0, tallyColumn, tallyLabel, header)
        tallyColumn += 1

    # Tally records
    tallyColumn = numLabels + numDays
    for k in range(1,row):
            worksheet.write_formula(k, tallyColumn, "=COUNTIF({}{}:{}{},\"<{}\")".format(deciToLetters(numLabels+1),k+1,deciToLetters(numLabels+numDays),k+1,rawTimeLate),default)
            worksheet.write_formula(k, tallyColumn+1, "=COUNTIF({}{}:{}{},\">={}\")".format(deciToLetters(numLabels+1),k+1,deciToLetters(numLabels+numDays),k+1,rawTimeLate),default)
            worksheet.write_formula(k, tallyColumn+2, "=COUNTBLANK({}{}:{}{})".format(deciToLetters(numLabels+1),k+1,deciToLetters(numLabels+numDays),k+1),default)
            worksheet.write_formula(k, tallyColumn+3, "=SUM({}{}:{}{})".format(deciToLetters(tallyColumn+1),k+1,deciToLetters(tallyColumn+3),k+1),default)

    # Color code late, absent, and present
    worksheet.conditional_format(deciToLetters(numLabels+1)+'2:'+deciToLetters(numDays+numLabels)+str(row),{'type':'blanks','format':gray})
    worksheet.conditional_format(deciToLetters(numLabels+1)+'2:'+deciToLetters(numDays+numLabels)+str(row),{'type':'time','criteria':'>=','value':timeLate,'format':red})
    worksheet.conditional_format(deciToLetters(numLabels+1)+'2:'+deciToLetters(numDays+numLabels)+str(row),{'type':'time','criteria':'<','value':timeLate,'format':green})

    worksheet.set_column(0,0,3)     #CN
    worksheet.set_column(1,3,12)    #Last and Middle Names
    worksheet.set_column(2,2,20)    #First Names
    worksheet.set_column(4,4,5)     #Sex
    worksheet.set_column(numLabels, numLabels+numDays,9)   #Attendance
    worksheet.set_column(tallyColumn,tallyColumn+4,7)     #Tally

    workbook.close()
    print(workbook.filename, "created.")



# Test if these functions work
if __name__ == "__main__":
    from ARFID_Database import *

    dbUser = "cs"
    dbName = "test"

    queries = setupQueries("students20", "tapRecords")
    cnx, cursor = setupDbCon(dbUser, dbName)

    sections = ['Hernandez','Banzon','Sycip']
    for section in sections:
        createExcelAttendance(section)