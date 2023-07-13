import os
from tkinter import *
import tkinter as tk
from tkinter import ttk
from PIL import Image,ImageTk  #used for jpeg,etc except png
from tkinter import messagebox as msg
import sqlite3
#========for pdf=============================
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from pyBSDate import convert_AD_to_BS
from tkcalendar import DateEntry


class salesEntryclass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1200x650+150+100")
        self.root.iconbitmap("image\panda.ico")
        self.root.title("Sales Entry")
        #high light open window
        self.root.focus_force()
        # Set the root window to be resizable
        self.root.resizable(True, True)

         # Initialize the counter variable
        self.counter = 1  
        self.total_row = None
        self.last_invoice_no = 0 
        self.branch_id = []  # Initialize branch_id as an instance variable
        self.invoice_number = self.fetch_last_invoice_number()
        
        
        #all variables
        self.bss=StringVar()
        self.brc=StringVar()
        self.var_id=IntVar()
        self.var_pan_no=StringVar()
        self.var_name=StringVar()
        self.inv_date=StringVar()
        self.item_type=StringVar()
        self.quantity=IntVar()
        self.rate_type=DoubleVar()
        self.amount=DoubleVar()
        self.discount_per=DoubleVar()
        self.discount_amt=DoubleVar()
        self.taxable_amt=DoubleVar()
        self.remark=StringVar()
      
        self.vat_amount=DoubleVar()
        #self.total_amt=IntVar()

        def handle_radio_selection():
            selected_option = self.var.get()
            if selected_option == 1:
                
                ppno_label.place_forget()
                self.ppno.place_forget() 
                label_country.place_forget() 
                self.exp_country.place_forget()
                lable_sellerpan.place_forget()
                self.selllerpan.place_forget()
            elif selected_option == 2:
                
                ppno_label.place(x=530,y=20)
                self.ppno.place(x=530, y=40, width=150)  # Display the entry box

                label_country.place(x=730,y=20)
                self.exp_country.place(x=730, y=40, width=150)

                lable_sellerpan.place(x=930,y=20)
                self.selllerpan.place(x=930,y=40,width=150)
        
        # Create a variable to hold the selected option
        self.var = IntVar(value=1)

        # Create the radio buttons
        radio_button1 = ttk.Radiobutton(self.root, text="Local", variable=self.var, value=1)
        radio_button2 = ttk.Radiobutton(self.root, text="Export", variable=self.var, value=2)

        # Create the entry box
        ppno_label=Label(self.root,text="P.P.No",font=("time new roman",10,"bold"))
        self.ppno = ttk.Entry(self.root)

        label_country=Label(self.root,text="Export Country",font=("time new roman",10,"bold"))
        self.exp_country = ttk.Entry(self.root)

        lable_sellerpan=Label(self.root,text="SellerPAN",font=("times new roman",10,"bold"))
        self.selllerpan=ttk.Entry(self.root)
       

        # Set a command that will be called when a radio button is selected
        self.var.trace("w", lambda *args: handle_radio_selection())

        # Pack the radio buttons onto the window
        radio_button1.place(x=40,y=33,width=80)
        radio_button2.place(x=150,y=35,width=80)

        #Invoice type
        # Create a frame to hold the combobox
        frame = Label(self.root,text="Invoice Type",font=("goudy old style",15)).place(x=300,y=3,width=200,height=55)
        self.Invc_type=ttk.Combobox(self.root,values=("VAT Invoice","Abbreviated Invoice"),state="readonly",justify="center",font=("times new roman",10,"bold"))
        self.Invc_type.place(x=320,y=40)
        placeholder = "Select Bill Type"
        self.Invc_type.set(placeholder)

        # #business
        # business = Label(self.root,text="Business",font=("goudy old style",15)).place(x=38,y=94)
        # self.bss=ttk.Combobox(self.root,textvariable=self.bss,state="readonly",justify="center",font=("times new roman",10,"bold"))
        # self.bss.place(x=40,y=120)
        # self.bss.bind("<<ComboboxSelected>>", self.on_bss_select)
        # #self.load_business_names()
        # self.bss.current(0)
        # #branch
        # branch = Label(self.root,text="*Branch",font=("goudy old style",15)).place(x=247,y=94)
        # brc_type=ttk.Combobox(self.root,textvariable=self.brc,state="readonly",justify="center",font=("times new roman",10,"bold"))
        # brc_type.place(x=250,y=120)
        # self.load_business_names()
        # #brc_type.current(0)
        
        business = Label(self.root, text="Business", font=("goudy old style", 15)).place(x=38, y=94)
        self.bss = ttk.Combobox(self.root, textvariable=self.bss, state="readonly", justify="center", font=("times new roman", 10, "bold"))
        self.bss.place(x=40, y=120)
        self.bss.bind("<<ComboboxSelected>>", self.on_bss_select)
        placeholder = "Select Business"
        self.bss.set(placeholder)

        # branch
        branch = Label(self.root, text="*Branch", font=("goudy old style", 15)).place(x=247, y=94)
        self.branch_combobox = ttk.Combobox(self.root, textvariable=self.brc, state="readonly", justify="center", font=("times new roman", 10, "bold"))
        self.branch_combobox.place(x=250, y=120)
        self.load_business_names()
        placeholder = "Select Branch"
        self.branch_combobox.set(placeholder)
       
        # Date
        Label(self.root, text="Date", font=("goudy old style", 15)).place(x=448, y=94)
        self.date_entry = DateEntry(self.root, width=20,height=30, background='darkblue',
                                    foreground='white', borderwidth=2)
        self.date_entry.place(x=450, y=120)
        self.date_entry.bind("<<DateEntrySelected>>", self.get_selected_date)

   
        
        
        #buyer pan
        buyer = Label(self.root,text="Buyer Pan",font=("goudy old style",15)).place(x=650,y=94)
        self.byr_pan=Entry(self.root,textvariable=self.var_pan_no,font=("time new roman", 10, "bold"))
        self.byr_pan.place(x=650,y=120,height=25)
        #byr_type.insert(0,"Buyer Pan")
        #buyer name
        
        buyer = Label(self.root,text="Buyer name",font=("goudy old style",15)).place(x=850,y=94)
        self.byr_name=Entry(self.root,textvariable=self.var_name,font=("time new roman", 10, "bold"))
        self.byr_name.place(x=850,y=120,height=25)
        #byr_type.insert(0,"Buyer name")

        #======menu===========
       
        # Item label
        items = Label(self.root, text="Item", font=("goudy old style", 15))
        items.place(x=35, y=150)
        self.item_type = tk.StringVar()
        self.item = ttk.Combobox(self.root, textvariable=self.item_type,values="select item", font=("time new roman", 10, "bold"))
        self.item.bind("<<ComboboxSelected>>", self.on_item_select)
        self.item.place(x=35, y=180, height=25)
        self.load_item_names()
        # Set the placeholder value
        placeholder = "Select an Item"
        self.item.set(placeholder)




        #quantity
        quantities = Label(self.root,text="Quantity",font=("goudy old style",15)).place(x=245,y=150)
        #self.quantity = DoubleVar()
        self.quantity=Entry(self.root,textvariable=self.quantity,font=("time new roman", 10, "bold"))
        self.quantity.bind("<KeyRelease>", self.update_amount)
        self.quantity.place(x=245,y=180,height=25)
        #rate
        rates = Label(self.root,text="Rate",font=("goudy old style",15)).place(x=445,y=150)
        #self.rate = DoubleVar()
        self.rate=Entry(self.root,textvariable=self.rate_type,font=("time new roman", 10, "bold"))
        self.rate.bind("<KeyRelease>", self.update_amount)
        self.rate.place(x=445,y=180,height=25)

        #Amount
        amounts = Label(self.root,text="Amount",font=("goudy old style",15)).place(x=645,y=150)
        self.amount=Entry(self.root,textvariable=self.amount,font=("time new roman", 10, "bold"))
        self.amount.place(x=645,y=180,height=25)

        #discount amount
        #discount_amount = Label(self.root,text="Discount Amount",font=("goudy old style",15)).place(x=845,y=150)
        self.dis_amt=Entry(self.root,textvariable=self.discount_amt,font=("time new roman", 10, "bold"))
        self.dis_amt.place(x=845,y=180,height=25)
        self.dis_amt.place_forget()


        #Taxable amount
        #txble_amt=Label(self.root,text="Taxable Amount",font=("goudy old style",15)).place(x=1045,y=150)
        self.taxable_amt=Entry(self.root,textvariable=self.taxable_amt,font=("time new roman", 10, "bold"))
        self.taxable_amt.place(x=1045,y=180,height=25)
        self.taxable_amt.place_forget()
        
       
        #vAT Amount
        #vat_amt= Label(self.root,text="Vat Amount",font=("goudy old style",14)).place(x=35,y=205)
        self.vat_amt=Entry(self.root,textvariable=self.vat_amount,font=("time new roman", 10, "bold"))
        self.vat_amt.place(x=35,y=230,height=25)
        self.vat_amt.place_forget()
        
        #Remark
       # remarks= Label(self.root,text="Remark",font=("goudy old style",15)).place(x=245,y=204)
        self.remanrk_bx=Entry(self.root,textvariable=self.remark,font=("time new roman", 10, "bold"))
        self.remanrk_bx.place(x=245,y=230,height=25,width=150)
        self.remanrk_bx.place_forget()
        

        #add button
        add_btn=Button(self.root,text="Add",font=("time new roman",15,"bold"),fg="white",bg="green",command=self.insert_row)
        add_btn.place(x=845,y=180,width=120,height=25)
        

     
        # #clear button
        # clear_btn=Button(self.root,text="Clear",font=("time new roman",15,"bold"),fg="white",bg="#D9905A",command=self.delete_selected_row)
        # clear_btn.place(x=1200,y=180,width=120,height=25)


        #billing table
        bill_frame=Frame(self.root,bd=3,relief=RIDGE)
        bill_frame.place(x=30,y=230,relwidth=0.96,height=180)

        scrolly=Scrollbar(bill_frame,orient=VERTICAL)
        scrollx=Scrollbar(bill_frame,orient=HORIZONTAL)

        self.BillTable=ttk.Treeview(bill_frame,columns=("SN","Item","Quantity","Rate","Amount","Discount Amount","Taxable Amount","Vat Amount","TaxExempt Amount","Total Amount","Remark","Action"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        #function of scrollbar
        scrollx.config(command=self.BillTable.xview)
        scrolly.config(command=self.BillTable.yview)
       

        self.BillTable.heading("SN",text="SN")
        self.BillTable.heading("Item",text="Item")
        self.BillTable.heading("Quantity",text="Quantity")
        self.BillTable.heading("Rate",text="Rate")
        self.BillTable.heading("Amount",text="Amount")
        self.BillTable.heading("Discount Amount",text="")#to hide remove text
        self.BillTable.heading("Taxable Amount",text="")#hide
        self.BillTable.heading("Vat Amount",text="")#hide
        self.BillTable.heading("TaxExempt Amount",text="TaxExempt Amount")
        self.BillTable.heading("Total Amount",text="Total Amount")
        self.BillTable.heading("Remark",text="")#hide
        self.BillTable.heading("Action",text="")#hide

        self.BillTable['show']="headings" #to hide default table

        self.BillTable.column("SN",width=40,anchor="center")
        self.BillTable.column("Item",width=200,anchor="center")
        self.BillTable.column("Quantity",width=100,anchor="center")
        self.BillTable.column("Rate",width=100,anchor="center")
        self.BillTable.column("Amount",width=150,anchor="center")
        self.BillTable.column("Discount Amount",width=0,anchor="center",stretch=False)#to hide width vlaue 0 and strech false
        self.BillTable.column("Taxable Amount",width=0,anchor="center",stretch=False)
        self.BillTable.column("Vat Amount",width=0,anchor="center",stretch=False)
        self.BillTable.column("TaxExempt Amount",width=100,anchor="center")
        self.BillTable.column("Total Amount",width=100,anchor="center")
        self.BillTable.column("Remark",width=0,anchor="center",stretch=False)
        self.BillTable.column("Action",width=0,anchor="center",stretch=False)
        self.BillTable.pack(fill=BOTH,expand=1)
      
        #styling of column
        s=ttk.Style()
        s.theme_use("clam")
        # Configure the style for the Treeview widget
        s.configure("Custom.Treeview", font=('Arial', 10), rowheight=25)

        # Apply the style to the Treeview widget=================================================
        self.BillTable.configure(style="Custom.Treeview")

   

   



#============================payment method radio button================================================

        paymentlabel=Label(self.root,text="Payment Mode",font=("time new roman",10,"bold")).place(x=35,y=420)
        
        
        # Create a variable to hold the selected option
        self.var1 = IntVar()

        # Create the radio buttons
        radio_button1 = ttk.Radiobutton(self.root, text="Cash", variable=self.var1, value=1)
        # radio_button2 = ttk.Radiobutton(self.root, text="Bank", variable=var1, value=2)
        # radio_button3 = ttk.Radiobutton(self.root, text="Online", variable=var1, value=3)

        #cash
        self.cas_label=Label(self.root,text="Receipt")
        self.cas_box=Entry(self.root,width=20)
        #Entry(self.root)
        #bank
        # bank_label=Label(self.root,text="Bank")
        # bank_box=Entry(self.root)
        # #cheque
        # ch_label=Label(self.root,text="Cheque No")
        # ch_box=Entry(self.root)
       

        # Set a command that will be called when a radio button is selected
        self.var1.trace("w", lambda *args: self.payment_radio_button())

        # Pack the radio buttons onto the window
        radio_button1.place(x=35,y=450,width=80)
        # radio_button2.place(x=150,y=590,width=80)
        # radio_button3.place(x=280,y=590,width=80)
#=========================================================================================================
        # Variable for Total SubTable
        # self.create_widgets()
        # self.populate_treeview()
        #  Create a Frame to hold the Treeview
        frames = Frame(self.root, bd=3,relief=RIDGE)  # Height calculation: 7 rows * row height + borderwidth
        frames.place(x=940, y=420,height=250, width=400,)


        self.tree = ttk.Treeview(frames, columns=("Summary", "Values"), show="headings")

        # Configure the Treeview style
        style = ttk.Style()
        style.configure("Custom.Treeview", font=('Arial', 10), borderwidth=3, relief=SOLID, rowheight=25)

        # Define custom tags for even and odd rows
        style.configure("Custom.Treeview.Item", background='#FFFFFF')
        style.configure("Custom.Treeview.Item.Even", background='#F2F2F2')

        # Configure the Treeview columns
        self.tree.heading("Summary", text="Summary")
        self.tree.heading("Values", text="Values")

        # Apply the tag configuration
        self.tree.tag_configure("even", background='#F2F2F2')
        
        # Set the font for the heading of each column
        style.configure("Treeview.Heading",
                 font=('Arial', 9, 'bold'))

        # Apply the style to the Treeview widget
        self.tree.configure(style="Custom.Treeview")

        self.tree.column("Summary", width=200, anchor="center")
        self.tree.column("Values", width=200, anchor="center")

        



        # Pack the Treeview widget
        self.tree.place(x=0, y=0, relwidth=1,relheight=1)
         # Apply the tag configuration
        self.tree.tag_configure("even", background='#CDCDC0')

             
 
#=====================Inserted row the total row BILLTABLE ===========================================================
        self.total_row = self.BillTable.insert("", "end", values=("", "Total", "", "", "","","","","","","",""), tags=("total"))
        #self.total_label = Label(root, text="Total Quantity: 0")
        
        # Move the total row to the bottom
        self.BillTable.move(self.total_row, "", "end")
        self.BillTable.tag_configure("total", font=("time new roman", 10, "bold"), background="#CDCDC0")
        style = ttk.Style()
        #style.configure("Treeview", rowheight=40)  # Set the row height for the entire Treeview widget
        
        self.BillTable.tag_bind("total_quantity", "<Button-1>", lambda event: "break")  # Disable selection of the total row
     
 
        
        tender=Entry(self.root,width=22,bd=1,relief="solid")
        tender.place(x=1200,y=575,height=25)
        change=Entry(self.root,width=22,bd=1,relief="solid")
        change.place(x=1200,y=602)
         #submit btn
        self.submit_btn=Button(self.root,text="Submit",font=("time new roman",15,"bold"),fg="white",bg="#3BB143",command=self.store_data)
        self.submit_btn.place(x=945,y=635,width=100,height=30)
        # Create the delete button
        delete_button = Button(self.root, text="Reset",font=('times new roman',15,"bold"),fg="white",bg="#D9905A", command= self.delete_all_rows)
        delete_button.place(x=1090, y=635,width=100,height=30)

        self.prt_invoice=Button(self.root, text="Print", font=("time new roman", 15, "bold"), fg="white", bg="#FF5733",command=self.generate_invoice,state=tk.DISABLED)
        self.prt_invoice.place(x=1235,y=635,width=100,height=30)
        
#=====================ALL FUNCTION AREA===============================================================
        self.is_vat=0
    def insert_row(self):
        
        itm = self.item_type.get()
        qnty = int(self.quantity.get() or 0)  # Convert to integer, defaulting to 0 if no value is entered
        rt = float(self.rate_type.get() or 0)   # Convert to integer, defaulting to 0 if no value is entered
        amt = float(self.amount.get() or 0)  # Convert to integer, defaulting to 0 if no value is entered
        disamt = float(self.discount_amt.get() or 0)  # Convert to integer, defaulting to 0 if no value is entered
        taxableamt=float(self.taxable_amt.get()or 0)
        vt = float(self.vat_amt.get() or 0)
        rm=self.remanrk_bx.get()
    
        taxableamt=amt-disamt
        if self.is_vat == 1:
            taxexmt = taxableamt + vt
            tamt = taxableamt + vt
        else:
            taxexmt = (qnty * rt)-disamt
            tamt = taxexmt
        
        #tamt = taxableamt + vt #===this row calculation
  
        self.BillTable.insert("", "end", values=(self.counter, itm, qnty, rt, amt, disamt, taxableamt, vt,taxexmt,tamt, rm,""))
        self.counter += 1  # Increment the counter

        conn=sqlite3.connect("gfd.db")
        cur=conn.cursor()
        cur.execute("SELECT IsVat FROM Items")
        self.is_vat = cur.fetchall()[0][0]
        conn.commit()
        conn.close()
    
        
        
        # Retrieve the selected option from the radio button
        selected_option = self.var.get()
        #print(selected_option)

    

       
        
        # Update the total row
        self.calculate_total()
        

        # Move the total row to the bottom
        if self.total_row:
            self.BillTable.move(self.total_row, "", "end")

      



    def calculate_total(self):
        total_quantity=0
        total_rate=0
        total_amount=0
        total_discount_amount=0
        total_taxable_amt=0
        total_vat_amt=0
        total_taxexmt=0
        net_amount=0
  
        for child in self.BillTable.get_children():
            if child != self.total_row:
                quantity = int(self.BillTable.item(child, 'values')[2])
                total_quantity += quantity

                rate = float(self.BillTable.item(child,'values')[3])
                total_rate+=rate

                amount=float(self.BillTable.item(child,'values')[4])
                total_amount+=amount

                disamt= float(self.BillTable.item(child,'values')[5])
                total_discount_amount+=disamt

                txamt=float(self.BillTable.item(child,'values')[6])
                total_taxable_amt+=txamt

                vat=float(self.BillTable.item(child,'values')[7])
                total_vat_amt+=vat

                taxemt=float(self.BillTable.item(child,'values')[8])
                total_taxexmt+=taxemt


                tamt=float(self.BillTable.item(child,'values')[9])
                net_amount+=tamt


        if not self.total_row:
            self.total_row = self.BillTable.insert("", "end", values=("", "Total", "", "", "", "", "", "", "", "", "",""), tags=("total"))

                
        # Update the total row with the calculated total quantity
        self.BillTable.set(self.total_row, "Quantity", total_quantity)
        self.BillTable.set(self.total_row, "Rate", total_rate)
        self.BillTable.set(self.total_row, "Amount", total_amount)
        #self.BillTable.set(self.total_row, "Discount", total_discount_per )
        self.BillTable.set(self.total_row, "Discount Amount", total_discount_amount )
        self.BillTable.set(self.total_row, "Taxable Amount", total_taxable_amt )
        self.BillTable.set(self.total_row, "Vat Amount", total_vat_amt )
        self.BillTable.set(self.total_row, "TaxExempt Amount", total_taxexmt )
        self.BillTable.set(self.total_row, "Total Amount", net_amount )

        # Retrieve values from the total row===============
        self.total_values = [
        "",
        "Total Amount",
        total_quantity,
        total_rate,
        total_amount,
        total_discount_amount,
        total_taxable_amt,
        total_vat_amt,
        total_taxexmt,
        net_amount,
        "",
        ""
    ]
        
      # Insert the rows if they don't exist already self.tree
      # Check if the summary rows already exist
        if not self.tree.exists("total_amount_row"):
      # Insert the "Total Amount" row at a fixed position
            self.tree.insert("", "end", values=("Total Amount", ""), tags="summary_row", iid="total_amount_row")

        if not self.tree.exists("total_discount_row"):
      # Insert the "Total Discount" row at a fixed position
            self.tree.insert("", "end", values=("Total Discount Amount", ""), tags="summary_row", iid="total_discount_row")

        if not self.tree.exists("total_taxable_row"):
      # Insert the "Total Quantity" row at a fixed position
            self.tree.insert("", "end", values=("Taxable Amount", ""), tags="summary_row", iid="total_taxable_row")

        if not self.tree.exists("total_vat_row"):
      # Insert the "Total Quantity" row at a fixed position
            self.tree.insert("", "end", values=("Total VAT Amount", ""), tags="summary_row", iid="total_vat_row")
     
        if not self.tree.exists("total_payable_row"):
      # Insert the "Total Quantity" row at a fixed position
            self.tree.insert("", "end", values=("Total Payable Amount", ""), tags="summary_row", iid="total_payable_row")
        
        if not self.tree.exists("total_tender_row"):
      # Insert the "Total Quantity" row at a fixed position
            self.tree.insert("", "end", values=("Tender Amount", ""), tags="summary_row", iid="total_tender_row")

        if not self.tree.exists("total_change_row"):
      # Insert the "Total Quantity" row at a fixed position
            self.tree.insert("", "end", values=("Changes Amount", ""), tags="summary_row", iid="total_change_row")

         
        
        if self.is_vat == 0:
            if not self.tree.exists("total_taxexmpt_amount"):
                self.tree.insert("", "end", values=("TaxExempt Amount", ""), tags="summary_row", iid='total_taxexmpt_amount_row')
            self.tree.set("total_taxexmpt_amount_row", "Values", self.total_values[8])

      
      # Update the "Total Amount" row
        self.tree.set("total_amount_row", "Values", self.total_values[4])
      # Update the "Total Discount" row
        self.tree.set("total_discount_row", "Values", self.total_values[5]) 
      # Update the "Total Quantity" row
        self.tree.set("total_taxable_row", "Values", self.total_values[6])  
        self.tree.set("total_vat_row", "Values", self.total_values[7])  
        self.tree.set("total_payable_row", "Values", self.total_values[9])  
        


        # Configure the tag for even rows to change their color
        self.tree.tag_configure("even_row", background="light gray")

        # Iterate over the rows and apply the tag to even rows
        for i, row in enumerate(self.tree.get_children()):
            if i % 2 == 1:
                self.tree.item(row, tags=("even_row",))
        
        
#==================DATE AND FISCAL YEAR=============================================================        

    # def get_selected_date(self,event):
    #     date = self.date_entry.get_date()
    #     bs_date = convert_AD_to_BS(date.year, date.month, date.day)
    #     # print(f"Selected date: {date}")
    #     # print(f"BS date: {bs_date}")

    #     fiscal_year = self.get_fiscal_year(bs_date)
    #     conn = sqlite3.connect("gfd.db")
    #     cur = conn.cursor()
    #     cur.execute("INSERT INTO SalesItems (FiscalYear) VALUES (?)", (fiscal_year,))
    #     conn.commit()
    #     conn.close()

        #print(f"Fiscal year: {fiscal_year}")
    
    def get_selected_date(self, event):
        date = self.date_entry.get_date()
        bs_date = convert_AD_to_BS(date.year, date.month, date.day)

        fiscal_year = self.get_fiscal_year(bs_date)
        conn = sqlite3.connect("gfd.db")
        cur = conn.cursor()

        # Get the last inserted invoice number
        cur.execute("SELECT MAX(InvoiceNo) FROM SalesItems")
        last_invoice_number = cur.fetchone()[0]

        # Update the fiscal year for the last inserted row
        #cur.execute("UPDATE SalesItems SET FiscalYear = ? WHERE InvoiceNo = ?", (fiscal_year, last_invoice_number))

        conn.commit()
        conn.close()

    def get_fiscal_year(self, bs_date):
        bs_year, bs_month, bs_day = bs_date  # Unpack the values from the tuple
        if bs_month >= 4:  # Assuming the fiscal year starts in Baisakh (April-May)
            #return bs_year + 1
            return f"{bs_year}/{bs_year + 1}"
        else:
            #return bs_year
            return f"{bs_year - 1}/{bs_year}"

#=====================================================================================================     
     #FUNCTION TO AUTO UPDATE AMOUNT FILED
    def update_amount(self, event):
        qty = int(self.quantity.get()or 0)
        rate = float(self.rate.get()or 0)
        amount = qty * rate
        self.amount.delete(0, tk.END)  # Clear the current content of the entry
        self.amount.insert(tk.END, float(amount))

  
#===============================load data in item field==============================================================

    #Insert in item tables and make it auto fill value
    def load_item_names(self, event=None):
        conn = sqlite3.connect('gfd.db')
        cursor = conn.cursor()

    # Retrieve the available item names from the database
        cursor.execute("SELECT DISTINCT NameEng FROM Items")
        item_names = [row[0] for row in cursor.fetchall()]
        conn.commit()

    # Set the item names in the combobox
        self.item['values'] = item_names
        
        
    # Close the database connection
        conn.close()
  
        

   
#==============================================================================================
    def on_item_select(self, event):
        selected_item = self.item.get()
    
        conn = sqlite3.connect('gfd.db')
        cursor = conn.cursor()

    # Retrieve data for the selected item
        cursor.execute("SELECT i.NameEng, ir.Rate, ir.VATAmt,ir.DisAmt FROM Items AS i JOIN Items_rate AS ir ON i.ItemCode = ir.ItemCode WHERE i.NameEng = ?", (selected_item,))
        data = cursor.fetchone()
        conn.commit()
        

    # Close the database connectionc
        conn.close()
    #display in the entry box of rate,vat_amt etc
        if data:
        
            self.rate_type.set(float(data[1])) #variable name not entrybox name (self.rate.type)
            
            self.vat_amount.set(float(data[2]))
            self.discount_amt.set(float(data[3]))
        else:
            self.rate_type.set('')
            self.vat_amount.set('')
            self.discount_amt.set('')
    #=============insert in Business===================================================================
     #Isert in item tables and make it auto fill value
    # def load_business_names(self, event=None):
    #     conn = sqlite3.connect('gfd.db')
    #     cursor = conn.cursor()

    # # Retrieve the available item names from the database
    #     cursor.execute("SELECT DISTINCT BusinessType FROM Business")
    #     business_names = [row[0] for row in cursor.fetchall()]
    #     conn.commit()

    # # Set the item names in the combobox
    #     self.bss['values'] = business_names
        
        
    # # Close the database connection
    #     conn.close()
    # #=====================on BUSINESS SELECTED=====================================================
  

    def load_business_names(self, event=None):
        conn = sqlite3.connect('gfd.db')
        cursor = conn.cursor()

        # Retrieve the available item names from the database
        cursor.execute("SELECT DISTINCT BusinessType FROM Business")
        business_names = [row[0] for row in cursor.fetchall()]
        conn.commit()

        # Set the item names in the combobox
        self.bss['values'] = business_names

        # Close the database connection
        conn.close()
    def on_bss_select(self, event):
        selected_item = self.bss.get()

        conn = sqlite3.connect('gfd.db')
        cursor = conn.cursor()

        # Retrieve data for the selected item
        cursor.execute("SELECT b.BusinessType, br.BranchName,br.BranchID FROM Business AS b JOIN Branch AS br ON b.BusinessID = br.BusinessID WHERE b.BusinessType = ?", (selected_item,))
        data = cursor.fetchall()

        # Extract branch names from the fetched data
        branch_names = [row[1] for row in data]
        self.branch_id=[row[2] for row in data]
        #print(self.branch_id)
        # Set the branch names in the branch combobox
        self.branch_combobox['values'] = branch_names
        

        conn.commit()
        conn.close()

     
    #delete all row from treeview================================================================
   
    def delete_all_rows(self):
    # Get all the item IDs in the Treeview
        item_ids = self.BillTable.get_children()

    # Delete each item from the Treeview
        for item_id in item_ids:
            self.BillTable.delete(item_id)
    
    # Reset the total row to None
        self.total_row = None

    # Get all the item IDs in the self.tree Treeview
        tree_item_ids = self.tree.get_children()

    # Delete each item from the self.tree Treeview
        for tree_item_id in tree_item_ids:
            self.tree.delete(tree_item_id)

        self.counter = 1

        #Clear the entry boxes
       
        self.item.delete(0, END)
        self.quantity.delete(0, END)
        self.rate.delete(0, END)
        self.amount.delete(0, END)
        self.dis_amt.delete(0, END)
        self.taxable_amt.delete(0, END)
        self.vat_amt.delete(0, END)
        self.remanrk_bx.delete(0,END)  #(use entry field name)
        self.ppno.delete(0,END)
        self.exp_country.delete(0,END)
        self.selllerpan.delete(0,END)
        self.byr_pan.delete(0,END)
        self.byr_name.delete(0,END)
          

    #payment radio btn
    def payment_radio_button(self):
            selected_option = self.var1.get()
            if selected_option == 1:
                
                self.cas_label.place(x=35,y=475)
                self.cas_box.place(x=35,y=500)
                # bank_label.place_forget()
                # bank_box.place_forget()
                # ch_label.place_forget()
                # ch_box.place_forget()
            # elif selected_option == 2:
                
            #     cas_label.place_forget()
            #     cas_box.place_forget()
            #     bank_label.place(x=35,y=625)
            #     bank_box.place(x=35,y=645)
            #     ch_label.place(x=220,y=625)
            #     ch_box.place(x=220,y=645)
            # elif selected_option == 3:
                
            #     cas_label.place_forget()
            #     cas_box.place_forget()
            #     bank_label.place_forget()
            #     bank_box.place_forget()
            #     ch_label.place_forget()
            #     ch_box.place_forget()
       

    
     
        
      
        

#=======================INVOICE NO=============================================
    


    def fetch_last_invoice_number(self):
        conn = sqlite3.connect("gfd.db")
        cur = conn.cursor()
        cur.execute("SELECT MAX(CAST(InvoiceNo AS INTEGER)) FROM SalesItems")
        result = cur.fetchone()
        conn.commit()
        conn.close()
        return int(result[0]) if result[0] else 0

  
    def generate_invoice_number(self):
        self.invoice_number = self.fetch_last_invoice_number() + 1
       #self.update_last_invoice_number(str(self.invoice_number))
        #print(f"Invoice Number: {self.invoice_number}")


     
   
    #===========generate bill===============================================================================
    def generate_invoice(self):
        bill_data = []
        for row in self.BillTable.get_children():
            sn = self.BillTable.item(row, "values")[0]
            item = self.BillTable.item(row, "values")[1]
            quantity = self.BillTable.item(row, "values")[2]
            rate = self.BillTable.item(row, "values")[3]
            amount = self.BillTable.item(row, "values")[4]
            discount_amt = self.BillTable.item(row, "values")[5]
            taxable_amt = self.BillTable.item(row, "values")[6]
            vat_amt = self.BillTable.item(row, "values")[7]
            total_amt = self.BillTable.item(row, "values")[8]

        bill_data.append({
            "sn": sn,
            "item": item,
            "quantity": quantity,
            "rate": rate,
            "amount": amount,
            "discount_amt": discount_amt,
            "taxable_amt": taxable_amt,
            "vat_amt": vat_amt,
            "total_amt": total_amt
        })

        self.generate_invoice_pdf()

    def generate_invoice_pdf(self):
        doc = SimpleDocTemplate("invoice.pdf", pagesize=letter)
        styles = getSampleStyleSheet()
        content = []

        content.append(Paragraph("Invoice", styles["Title"]))
    
        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        content.append(Paragraph(f"Date: {current_datetime}", styles["Normal"]))
    
        content.append(Paragraph(f"Invoice Number: {self.invoice_number}", styles["Normal"]))
    
        content.append(Spacer(1, 12))

        data = [
            ["SN", "Item", "Quantity", "Rate", "Amount", "Discount", "Taxable", "VAT", "Total"]
                ]

        for row in self.BillTable.get_children():
            sn = self.BillTable.item(row, "values")[0]
            item = self.BillTable.item(row, "values")[1]
            quantity = self.BillTable.item(row, "values")[2]
            rate = self.BillTable.item(row, "values")[3]
            amount = self.BillTable.item(row, "values")[4]
            discount_amt = self.BillTable.item(row, "values")[5]
            taxable_amt = self.BillTable.item(row, "values")[6]
            vat_amt = self.BillTable.item(row, "values")[7]
            total_amt = self.BillTable.item(row, "values")[8]

            data.append([
                sn,
                item,
                quantity,
                rate,
                amount,
                discount_amt,
                taxable_amt,
                vat_amt,
                total_amt
            ])

        table = Table(data)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), "grey"),
            ("TEXTCOLOR", (0, 0), (-1, 0), "white"),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 12),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), "white"),
            ("GRID", (0, 0), (-1, -1), 1, "black"),
        ]))

        content.append(table)
    
        doc.build(content)
    
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"invoice_{timestamp}.pdf"
    
        destination = os.path.join(os.getcwd(), "Receipt", filename)
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        os.rename("invoice.pdf", destination)
    
        msg.showinfo("Success", "Invoice generated successfully!")

#===================FUN TO GET ITEM ID FROM ITEM TABLE==================================================================
    def get_item_id(self, item_name):
        conn = sqlite3.connect("gfd.db")
        cur = conn.cursor()
        cur.execute("SELECT ItemCode FROM Items WHERE NameEng = ?", (item_name,))
        result = cur.fetchone()
        conn.close()
        return result[0] if result else None
    
    def get_branch_id(self, branch_name):
        conn = sqlite3.connect("gfd.db")
        cur = conn.cursor()
        cur.execute("SELECT BranchID FROM Branch WHERE BranchName = ?", (branch_name,))
        result = cur.fetchone()
        conn.close()
        return result[0] if result else None
    
    def get_pan(self, pan):
        conn = sqlite3.connect("gfd.db")
        cur = conn.cursor()
        cur.execute("SELECT PanNo FROM Business WHERE BusinessType = ?", (pan,))
        result = cur.fetchone()
        conn.close()
        return result[0] if result else None




   
#=============================INSERT INTO DATABASE=======================================================================
    
    def store_data(self):
        
        self.generate_invoice_number()#done
        self.get_selected_date(None)

        # Get the selected item and retrieve its ItemId
        selected_item = self.item_type.get()
        item_id = self.get_item_id(selected_item)
    
        # Get the selected Branch and retrieve its BranchId
        selected_branch = self.brc.get()  #get branch variable
        branch_id = self.get_branch_id(selected_branch) #get function
        # Get the selected Branch and retrieve its BranchId
        selected_bussinessType = self.bss.get()  #get branch variable
        pan_no = self.get_pan(selected_bussinessType) #get function
        print(pan_no)
        
        
        # Get the AD date from the input (assuming it's a string)
        ad_date_str=self.date_entry.get_date()
        # Convert the AD date to a string
        ad_date_str = str(ad_date_str)
        # Convert the AD date to a Python `date` object
        ad_date = datetime.datetime.strptime(ad_date_str, "%Y-%m-%d").date()

        # Convert the AD date to BS
        bs_date = convert_AD_to_BS(ad_date.year, ad_date.month, ad_date.day)
        # Convert bs_date tuple to a string
        bs_date_str = "-".join(str(part) for part in bs_date)


        


        buyerpan=self.byr_pan.get()
        buyername=self.byr_name.get()
        exportppno=self.ppno.get()
        export_country=self.exp_country.get()
        sellerpan=self.selllerpan.get()
        billtypeid=self.Invc_type.get()
        




        rate = float(self.rate_type.get() or 0)
        qty = int(self.quantity.get()or 0)
        total_amount = self.tree.set("total_amount_row", "Values")
        discount=self.tree.set("total_discount_row", "Values") 
        taxable=self.tree.set("total_taxable_row", "Values") 
        tax=self.tree.set("total_vat_row", "Values")  
        taxExmpt=self.tree.set("total_payable_row", "Values") 

        # Get the complete fiscal year
        #fiscal_year = self.get_fiscal_year(convert_AD_to_BS(date.year, date.month, date.day))
        # Get the fiscal year
        fiscal_year = self.get_fiscal_year(bs_date)


        # Get the selected radio button option
        selected_option = self.var.get()

          
        # Establish a connection to the SQLite database
        conn = sqlite3.connect("gfd.db")

        # Create a cursor object to interact with the database
        cur = conn.cursor()

        try:
            if selected_option == 1:
            # Set exportedamount to NULL for the selected rows
            
                cur.execute("INSERT INTO SalesItems (InvoiceNO,FiscalYear,ItemId,Quantity, Rate, TotalAmount, DiscountAmount, TaxableAmount,TaxAmount,TaxExemptAmount) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (self.invoice_number, fiscal_year, item_id, qty, rate,total_amount,discount,taxable,tax,taxExmpt))
                # Commit the changes to the database
                conn.commit()
                 # Insert the data into the database table
                cur.execute("INSERT INTO SalesRegisters (BillDate,InvoiceNO,SellerPAN,BuyerName,BuyerPAN,FiscalYear,EntryBy,EntryDate,BranchId, BillTypeId, TotalAmount, TotalDiscountAmount, TotalTaxableAmount,TotalTaxAmount,TotalTaxExemptAmount,isRealTime,datetimeClient) VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (bs_date_str,self.invoice_number,sellerpan,buyername,buyerpan, fiscal_year,"",bs_date_str, branch_id, billtypeid,total_amount,discount,taxable,tax,taxExmpt,"", bs_date_str))
                # Commit the changes to the database
                conn.commit()
            elif selected_option == 2:
            # Insert new records with all fields populated
                cur.execute("INSERT INTO SalesItems (InvoiceNO,FiscalYear,ItemId,Quantity, Rate, TotalAmount, DiscountAmount, TaxableAmount,TaxAmount,TaxExemptAmount,ExportAmount) VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (self.invoice_number, fiscal_year, item_id, qty, rate,total_amount,discount,taxable,tax,taxExmpt,taxExmpt))
                # Commit the changes to the database
                conn.commit()

                # Insert the data into the database table
                cur.execute("INSERT INTO SalesRegisters (BillDate,InvoiceNO,SellerPAN,BuyerName,BuyerPAN,FiscalYear,EntryBy,EntryDate,BranchId,ExportPPDate,ExportPPNo, BillTypeId, TotalAmount, TotalDiscountAmount, TotalTaxableAmount,TotalTaxAmount,TotalTaxExemptAmount,TotalExportAmount,ExportedCountryName,isRealTime,datetimeClient) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?)",
                    (bs_date_str,self.invoice_number,sellerpan,buyername,buyerpan, fiscal_year,"",bs_date_str, branch_id,bs_date_str, exportppno, billtypeid,total_amount,discount,taxable,tax,taxExmpt,taxExmpt, export_country,"", bs_date_str))
                # Commit the changes to the database
                conn.commit()
            msg.showinfo("Success", "Submitted successfully!")

        except sqlite3.Error as e:
            # Handle any database errors
            print("Error occurred:", e)

        finally:
            # Close the database connection
            conn.close()
        
        self.prt_invoice.config(state=tk.NORMAL)
       

       
    
    
           
if __name__ == "__main__":

    root=Tk()
    obj=salesEntryclass(root)
    root.mainloop()