import sqlite3
import pandas as pd
import wx, wx.grid

# columns
columns = ['CAMIS', 'DBA', 'BORO', 'BUILDING', 'STREET', 'ZIPCODE', 'PHONE', 'CUISINE_DESCRIPTION', 'INSPECTION_DATE', 'ACTION', 'VIOLATION_CODE', 'VIOLATION_DESCRIPTION', 'CRITICAL_FLAG', 'SCORE', 'GRADE', 'GRADE_DATE', 'RECORD_DATE', 'INSPECTION_TYPE']

# conect with dataset
con = sqlite3.connect('NYC_Restaurant.db')
# cursor
cur = con.cursor()

# creat table
def create_table(cur):
    try:
        # sql query
        with open('create_table.sql', 'r') as f:
            sql = f.read()
        # 执行
        cur.execute(sql)
        print('DatasetCompleted！')
    except:
        print('DataExist！')

# table insert
def insert_table(cur, con):
    try:
        # sql query
        sql = 'select * from NYC_Restaurant_Inspections'
        cur.execute(sql)
        # results
        res = cur.fetchall()
        if len(res) > 0:
            print('DatasetAlreadyExist！')
        else:
            # read csv
            data = pd.read_csv('DOHMH_New_York_City_Restaurant_Inspection_Results.csv')
            # dataformat
            data['INSPECTION_DATE'] = data['INSPECTION_DATE'].apply(lambda x: '' if pd.isna(x) else x.split('/')[2] + x.split('/')[0] + x.split('/')[1])
            data['GRADE_DATE'] = data['GRADE_DATE'].apply(lambda x: '' if pd.isna(x) else x.split('/')[2] + x.split('/')[0] + x.split('/')[1])
            data['RECORD_DATE'] = data['RECORD_DATE'].apply(lambda x: '' if pd.isna(x) else x.split('/')[2] + x.split('/')[0] + x.split('/')[1])
            # data to sql
            data.to_sql('NYC_Restaurant_Inspections', con=con, if_exists='replace', index=False)
            print('DataInsertCompleted！')
    except:
        print('NotExist！')

# define table
class MyGridTable(wx.grid.GridTableBase):
    def __init__(self, sql):
        super().__init__()
        self.sql = sql
        cur.execute(self.sql)
        self.data = cur.fetchall()
        self.colLabels = columns
    def GetNumberRows(self):
        return len(self.data)
    def GetNumberCols(self):
        return len(self.colLabels)
    def GetValue(self, row, col):
        return self.data[row][col]
    def GetColLabelValue(self, col):
        return self.colLabels[col]

# Button1
def fun1(event):
    # Close main window
    global mainWindow
    # close main window
    mainWindow.Close()
    # class define
    class window(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None, title="NYC", size=(1200, 800))
            # initialsql
            self.sql = "select * from NYC_Restaurant_Inspections limit 20"
            # define panel
            self.panel = wx.Panel(self)
            # define component
            self.mainButton = wx.Button(self.panel, label='Time', size=(150, 100))
            self.text1 = wx.StaticText(self.panel, label='StartDate', size=(60, 50))
            self.text2 = wx.StaticText(self.panel, label='EndDate', size=(60, 50))
            self.file1 = wx.TextCtrl(self.panel, size=(150, 30), name="8888")
            self.file2 = wx.TextCtrl(self.panel, size=(150, 30), name="8888")
            self.searchButton = wx.Button(self.panel, label='Find', size=(100, 50))
            self.grid = wx.grid.Grid(parent=self.panel)
            # layout(sizer)
            self.sizer1 = wx.BoxSizer(wx.HORIZONTAL)
            self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
            self.sizer3 = wx.BoxSizer(wx.VERTICAL)
            self.sizer4 = wx.BoxSizer(wx.HORIZONTAL)
            self.sizer5 = wx.BoxSizer(wx.VERTICAL)
            # layout
            self.get_set()
            # buttonbind
            self.mainButton.Bind(wx.EVT_BUTTON, main)
            self.searchButton.Bind(wx.EVT_BUTTON, self.search)

        def search(self, event):
            if len(self.file1.GetValue()) == 8 and len(self.file2.GetValue()) == 8:
                self.sql = "select * from NYC_Restaurant_Inspections where INSPECTION_DATE between {} and {} limit 100".format(self.file1.GetValue(), self.file2.GetValue())
                # layout
                self.get_set()

        def get_set(self):
            # tableset
            table = MyGridTable(self.sql)
            self.grid.SetTable(table, True)
            self.grid.AutoSize()
            # layout size
            self.sizer1.Add(self.text1, flag=wx.ALL, border=5)
            self.sizer1.Add(self.file1, flag=wx.ALL, border=5)
            self.sizer2.Add(self.text2, flag=wx.ALL, border=5)
            self.sizer2.Add(self.file2, flag=wx.ALL, border=5)
            self.sizer3.Add(self.sizer1, flag=wx.ALL, border=5)
            self.sizer3.Add(self.sizer2, flag=wx.ALL, border=5)
            self.sizer4.Add(self.mainButton, flag=wx.ALL | wx.CENTER, border=20)
            self.sizer4.Add(self.sizer3, flag=wx.ALL | wx.CENTER, border=20)
            self.sizer4.Add(self.searchButton, flag=wx.ALL | wx.CENTER, border=20)
            self.sizer5.Add(self.sizer4, flag=wx.ALL, border=5)
            self.sizer5.Add(self.grid, flag=wx.ALL, border=5)
            # layout
            self.panel.SetSizer(self.sizer5)

    # window
    window = window()
    # window.show
    window.Show()
    # mainwindow
    mainWindow = window

# Button2
def fun2(event):
    # mainwindow
    global mainWindow
    # close mian window
    mainWindow.Close()
    # window frame
    class window(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None, title="NYC", size=(1200, 800))
            # Initialsql
            self.sql = "select * from NYC_Restaurant_Inspections limit 20"
            # panelset
            self.panel = wx.Panel(self)
            # define componse
            self.mainButton = wx.Button(self.panel, label='Violation Distribution', size=(150, 100))
            self.text1 = wx.StaticText(self.panel, label='StartDate', size=(60, 50))
            self.text2 = wx.StaticText(self.panel, label='EndDate', size=(60, 50))
            self.file1 = wx.TextCtrl(self.panel, size=(150, 30), name="8888")
            self.file2 = wx.TextCtrl(self.panel, size=(150, 30), name="8888")
            self.searchButton = wx.Button(self.panel, label='Find', size=(100, 50))
            self.image = wx.StaticBitmap(self.panel, -1, wx.Bitmap("./1.jpeg", wx.BITMAP_TYPE_ANY))
            # layout size
            self.sizer1 = wx.BoxSizer(wx.HORIZONTAL)
            self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
            self.sizer3 = wx.BoxSizer(wx.VERTICAL)
            self.sizer4 = wx.BoxSizer(wx.HORIZONTAL)
            self.sizer5 = wx.BoxSizer(wx.VERTICAL)
            # layout
            self.get_set()
            # buttonBind
            self.mainButton.Bind(wx.EVT_BUTTON, main)
            self.searchButton.Bind(wx.EVT_BUTTON, self.search)

        def search(self, event):
            print(1111)

        def get_set(self):
            # layout size
            self.sizer1.Add(self.text1, flag=wx.ALL, border=5)
            self.sizer1.Add(self.file1, flag=wx.ALL, border=5)
            self.sizer2.Add(self.text2, flag=wx.ALL, border=5)
            self.sizer2.Add(self.file2, flag=wx.ALL, border=5)
            self.sizer3.Add(self.sizer1, flag=wx.ALL, border=5)
            self.sizer3.Add(self.sizer2, flag=wx.ALL, border=5)
            self.sizer4.Add(self.mainButton, flag=wx.ALL | wx.CENTER, border=20)
            self.sizer4.Add(self.sizer3, flag=wx.ALL | wx.CENTER, border=20)
            self.sizer4.Add(self.searchButton, flag=wx.ALL | wx.CENTER, border=20)
            self.sizer5.Add(self.sizer4, flag=wx.ALL, border=5)
            self.sizer5.Add(self.image, flag=wx.ALL, border=5)
            # layout
            self.panel.SetSizer(self.sizer5)

    # windowed
    window = window()
    # window show
    window.Show()
    # mainwindow
    mainWindow = window

# Button3
def fun3(event):
    # mainwindow
    global mainWindow
    # closewindow
    mainWindow.Close()
    # windowframe
    class window(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None, title="NYC", size=(1200, 800))
            # initialsql
            self.sql = "select * from NYC_Restaurant_Inspections limit 20"
            # panerl
            self.panel = wx.Panel(self)
            # define componese
            self.mainButton = wx.Button(self.panel, label='Violation Keyword', size=(150, 100))
            self.text = wx.StaticText(self.panel, label='Keyword', size=(60, 50))
            self.file = wx.TextCtrl(self.panel, size=(150, 30), name="8888")
            self.searchButton = wx.Button(self.panel, label='Find', size=(100, 50))
            self.grid = wx.grid.Grid(parent=self.panel)
            # layout size
            self.sizer4 = wx.BoxSizer(wx.HORIZONTAL)
            self.sizer5 = wx.BoxSizer(wx.VERTICAL)
            # layout
            self.get_set()
            # buttonbind
            self.mainButton.Bind(wx.EVT_BUTTON, main)
            self.searchButton.Bind(wx.EVT_BUTTON, self.search)

        def search(self, event):
            self.sql = "select * from NYC_Restaurant_Inspections where VIOLATION_DESCRIPTION like '%{}%' limit 100".format(self.file.GetValue())
            # layout
            self.get_set()

        def get_set(self):
            # tablesetting
            table = MyGridTable(self.sql)
            self.grid.SetTable(table, True)
            self.grid.AutoSize()
            # layout size
            self.sizer4.Add(self.mainButton, flag=wx.ALL | wx.CENTER, border=20)
            self.sizer4.Add(self.text, flag=wx.ALL | wx.CENTER, border=5)
            self.sizer4.Add(self.file, flag=wx.ALL | wx.CENTER, border=5)
            self.sizer4.Add(self.searchButton, flag=wx.ALL | wx.CENTER, border=20)
            self.sizer5.Add(self.sizer4, flag=wx.ALL, border=5)
            self.sizer5.Add(self.grid, flag=wx.ALL, border=5)
            # layout
            self.panel.SetSizer(self.sizer5)

    # windowed
    window = window()
    # window show
    window.Show()
    # mainwindow
    mainWindow = window

# Button5
def fun5(event):
    # mainwindow
    global mainWindow
    # windowclose
    mainWindow.Close()
    # window frame
    class window(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None, title="NYC", size=(1200, 800))
            # initialsql
            self.sql = "select * from NYC_Restaurant_Inspections limit 20"
            # panel
            self.panel = wx.Panel(self)
            # define component
            self.mainButton = wx.Button(self.panel, label='Borough', size=(150, 100))
            self.select = wx.ComboBox(self.panel, value='MANHATTAN', choices=['MANHATTAN', 'BRONX', 'BROOKLYN', 'QUEENS', 'STATEN ISLAND'], style=wx.CB_SORT)
            self.searchButton = wx.Button(self.panel, label='点击查询', size=(100, 50))
            self.grid = wx.grid.Grid(parent=self.panel)
            # layout size
            self.sizer4 = wx.BoxSizer(wx.HORIZONTAL)
            self.sizer5 = wx.BoxSizer(wx.VERTICAL)
            # layout
            self.get_set()
            # buttonbind
            self.mainButton.Bind(wx.EVT_BUTTON, main)
            self.searchButton.Bind(wx.EVT_BUTTON, self.search)

        def search(self, event):
            self.sql = "select * from NYC_Restaurant_Inspections where BORO = '{}' limit 100".format(self.select.GetValue())
            # layout
            self.get_set()

        def get_set(self):
            # tablesetting
            table = MyGridTable(self.sql)
            self.grid.SetTable(table, True)
            self.grid.AutoSize()
            # layout size
            self.sizer4.Add(self.mainButton, flag=wx.ALL | wx.CENTER, border=20)
            self.sizer4.Add(self.select, flag=wx.ALL | wx.CENTER, border=20)
            self.sizer4.Add(self.searchButton, flag=wx.ALL | wx.CENTER, border=20)
            self.sizer5.Add(self.sizer4, flag=wx.ALL, border=5)
            self.sizer5.Add(self.grid, flag=wx.ALL, border=5)
            # layout
            self.panel.SetSizer(self.sizer5)

    # windowed
    window = window()
    # windowshow
    window.Show()
    # mainwindow
    mainWindow = window


def main(event):
    # mainwindow
    global mainWindow
    # closewindow or not
    if mainWindow == None:
        pass
    else:
        mainWindow.Close()
    # window frame
    window = wx.Frame(None, title="NYC", size=(1200, 800))
    # pannelset
    panel = wx.Panel(window)
    # layout VERTICAL/HORIZONTAL
    sizer = wx.BoxSizer(wx.VERTICAL)
    # define component
    button1 = wx.Button(panel, label='Time', size=(150, 100))
    button2 = wx.Button(panel, label='Violation Distribution', size=(150, 100))
    button3 = wx.Button(panel, label='Violation Keyword', size=(150, 100))
    button4 = wx.Button(panel, label='Button4', size=(150, 100))
    button5 = wx.Button(panel, label='Borough', size=(150, 100))
    # layoutadd
    sizer.Add(button1, proportion=0, flag=wx.ALL | wx.CENTER, border=20)
    sizer.Add(button2, proportion=0, flag=wx.ALL | wx.CENTER, border=20)
    sizer.Add(button3, proportion=0, flag=wx.ALL | wx.CENTER, border=20)
    sizer.Add(button4, proportion=0, flag=wx.ALL | wx.CENTER, border=20)
    sizer.Add(button5, proportion=0, flag=wx.ALL | wx.CENTER, border=20)
    # buttonbind
    button1.Bind(wx.EVT_BUTTON, fun1)
    button2.Bind(wx.EVT_BUTTON, fun2)
    button3.Bind(wx.EVT_BUTTON, fun3)

    button5.Bind(wx.EVT_BUTTON, fun5)
    # layout
    panel.SetSizer(sizer)
    # window
    window.Show()
    # mainwindow
    mainWindow = window

# startapp
app = wx.App()
mainWindow = None
main(None)
# main loop
app.MainLoop()