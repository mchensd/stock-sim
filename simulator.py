from tkinter import *
import random

class Main(Frame):
    '''
    The main frame which holds all widgets
    '''
    def __init__(self, master, days):
        Frame.__init__(self, master, bg="#9da6b5")
        
        self.grid(sticky=N+S+E+W)
        
        self.days = days + 1  # calling update days reduces self.days by 1
        self.money = 1000
        self.normFont = ("Courier New", 12)
        
        
        self.createWidgets()
        self.updateDay()

    def createWidgets(self):
        
        self.tFrame = Frame(self, bg="#9da6b5")  # title frame
        self.tFrame.grid(columnspan=2, sticky=N, pady=15)        

        self.title = Label(self.tFrame, text="Welcome to Drug Simulator", font=("Courier New", 24, "bold"), bg="#9da6b5")
        self.title.grid(sticky=W+E, padx=20, pady=10)

        self.mLabel = Label(self.tFrame, text="Your money: {}".format(self.money), font=self.normFont, bg="#9da6b5")
        self.mLabel.grid(sticky=W+E)

        self.daysLabel = Label(self.tFrame, font=self.normFont, bg="#9da6b5")
        self.daysLabel.grid()
        
            

        self.nextDay = Button(self.tFrame, text="Next Day", command=self.updateDay, font=("Courier New", 12, "bold"), bg="#9da6b5" )
        self.nextDay.grid()
        
        self.menu = BuyMenu(self)
        self.menu.grid(row=2, column=0, pady=15, sticky=E+W+N+S,)

        self.inv = Inventory(self)
        self.inv.grid(row=2, column=1, pady=15, sticky=E+W+N+S,)# sticky=E)  

         

    def updateDay(self):
        '''
        Decrement day
        Update prices (possibility of anomalies) (TODO)
        Warning of 5 days left
        Check if days = 0 : end game/ask for restart
        '''        
    
        self.days -= 1

        if self.days == 5:
            messagebox.showwarning(title="Message", message="You have 5 days left!")

        elif self.days == 0:
            messagebox.showinfo(title="Congratulations!", message="You completed the drug dealer challenge with {} dollars".format(self.money))
            self.deactivate()
            
        if self.menu.drugMenu.curselection():  # deselect any current selections
            i = self.menu.drugMenu.curselection()[0]
            self.menu.drugMenu.selection_clear(first=i)
        elif self.inv.inventory.curselection():
            i = self.inv.inventory.curselection()[0]
            self.inv.inventory.selection_clear(first=i)
        
        self.daysLabel['text'] = "Days Left: {}".format(self.days)
        #change prices
        self.menu.updatePrices()

    def purchase(self, drugI, amount, cost):
        # called by self.menu when buy it is pressed
        self.inv.userInv[drugI] += amount
        self.money -= cost
        
        self.mLabel['text'] = "Your money: {}".format(self.money)
        self.inv.amounts.delete(drugI)
        self.inv.amounts.insert(drugI, self.inv.userInv[drugI])
        
        
    def sell(self, drugI, amount):
        # called by self.in when sell it is pressed
        cost = self.menu.prices[drugI] * amount
        self.money += cost
        self.mLabel['text'] = "Your money: {}".format(self.money)

    def deactivate(self):
        ''' Finish the game so the user can't do anything more'''
        self.menu.buy['state'] = DISABLED
        self.inv.sell['state'] = DISABLED
        self.nextDay['state'] = DISABLED
        
class BuyMenu(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, bg="#9da6b5") #, width=200, height=200) # testing
        self.master=master
        self.grid(padx=50)  # separates it from sell menu
        
        self.drugList = ["Weed", "Shrooms", "Heroin", "Cocaine", "Crack", "Acid", "Opium", "Speed"]
        self.createWidgets()
        #self.grid_propagate(0)

    def createWidgets(self):
        
        self.menuFont = ("Courier New", 10)
        self.menuTitle = Label(self, text="Today's menu", font=("Courier New", 12, "underline"))
        self.menuTitle.grid(row=0, column=0)
        

        self.drugMenu = Listbox(self, height=8, selectmode=SINGLE, activestyle="none", font=self.menuFont,width=17)
        self.drugMenu.grid(row=1, column=0, padx=5, pady=(3,10))

        for d in self.drugList:
            self.drugMenu.insert(END, d)

        self.pTitle = Label(self, text="Prices", font=("Courier New", 12, "underline"))
        self.pTitle.grid(row=0, column=1)
        
        self.priceList = Listbox(self, activestyle="none", height=8, selectbackground="#ffffff", selectforeground="black", takefocus=0,
                              font=self.menuFont, width=10)
        self.priceList.grid(row=1, column=1, pady=(3,10))

        self.buy = Button(self, text="Buy it!", command=self.buyDrugs)
        self.buy.grid(row=2, column=0, columnspan=2)

    def updatePrices(self):
        self.prices = self.generatePrices()
        for i in range(len(self.prices)):
            self.priceList.insert(i, self.prices[i])
        
    def generatePrices(self):
        
        weed = random.randint(200,700)
        shrooms = random.randint(400,1000)
        heroin = random.randint(2013, 7692)
        cocaine = random.randint(10234, 18290)
        crack = random.randint(3500,7690)
        acid = random.randint(567, 1403)
        opium = random.randint(3251, 7882)
        speed = random.randint(67,315)
        #TODO: anomalies
        
        return [weed, shrooms, heroin, cocaine, crack, acid, opium, speed]

    def buyDrugs(self):
        try: drugI = self.drugMenu.curselection()[0]  # checks if the user selected a drug
        except:
            messagebox.showwarning(title="Error", message="Please select a drug to buy")
            return

        w = PopupInput(self.master, money=self.master.money, drug=self.drugList[drugI], drugPrice = self.prices[drugI], buy=True, )
        # Asks for how much the user wants to buy
        self.master.wait_window(w.top)
        try:
            amount = w.amount
            cost = amount*self.prices[drugI]
            self.master.purchase(drugI, amount, cost)  # updates money AND inventory
        except:  # if cancel is pressed, w.amount is not set
            return
        
        #Label(self, text="Hello Label").grid()

    

class Inventory(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, bg="#9da6b5")# width=200, height=200, bg="#00ffff")
        self.grid(padx=50)
        
        self.drugList = ["Weed", "Shrooms", "Heroin", "Cocaine", "Crack", "Acid", "Opium", "Speed"]
        self.userInv = [0 for i in range(8)]

        
        self.menuFont = ("Courier New", 10)
        self.createWidgets()
        
        #self.grid_propagate(0)

    def createWidgets(self):     

        Label(self, text="Your Inventory", font=("Courier New", 12, "underline")).grid()

        self.inventory = Listbox(self, height=0, font=self.menuFont, width=18, activestyle="none")
        self.inventory.grid(row=1, column=0, padx=5, pady=(3,10))
        
        for i in self.drugList:
            self.inventory.insert(END, i)

        Label(self, text="Amounts", font=("Courier New", 12, "underline")).grid(row=0, column=1)
        
        self.amounts = Listbox(self, height=0, font=self.menuFont, width=10, activestyle='none', selectbackground="#ffffff", selectforeground="black")
        self.amounts.grid(row=1, column=1, pady=(3,10))
        for i in range(8):
            self.amounts.insert(END, 0)

        self.sell = Button(self, text="Sell it!", command=self.sellDrugs)
        self.sell.grid(row=2, column=0, columnspan=2)

        
    def sellDrugs(self):
        try: # check if user selected something
            drugI = self.inventory.curselection()[0]
        except:
            messagebox.showerror(title="Error", message="Please select a drug to sell")
            return

        w = PopupInput(self.master, self.master.money, self.drugList[drugI], self.master.menu.prices[drugI], buy=False, drugI=drugI)
        self.master.wait_window(w.top)
        try:
            numSell = w.amount
            self.master.sell(drugI, numSell)  # updates the amount of mmoney

            #updates the amount of drugs in inventory
            self.userInv[drugI] -= numSell
            self.amounts.delete(drugI)
            self.amounts.insert(drugI, self.userInv[drugI])
        
        except:
            return
    


class PopupInput(Frame):
    def __init__(self, master, money, drug, drugPrice, buy=True, drugI=None):
        # if buy is true, user is buying, else user is selling
        Frame.__init__(self, master)
        self.grid()
        self.master = master
        
        okayCommand = (self.register(self.isOkay), "%S")
        self.drugI = drugI
        
        self.money = money
        self.drug = drug
        self.drugPrice = drugPrice
        self.defFont = ("Courier New", 12)
        self.bOrS = "buy" if buy else "sell"
        self.top = Toplevel(master)
        self.howMuch = Label(self.top, text="How much {} would you like to {}?".format(drug, self.bOrS), font=self.defFont)
        self.howMuch.grid(padx=20, pady=(5,0), columnspan=2)

        self.userInp = Entry(self.top, font=self.defFont, validate='key', validatecommand=okayCommand)

        self.userInp.grid(columnspan=2)
    
        if buy:
            self.userInp.insert(0, self.money // self.drugPrice)
        elif not buy:
            self.userInp.insert(0, self.master.inv.userInv[drugI])
        

        self.ok = Button(self.top, text="Ok", font=self.defFont, command=self.confirmOrder)
        self.ok.grid(ipadx=25)

        self.cancel = Button(self.top, text="Cancel", font=self.defFont, command=self.destroy)
        self.cancel.grid(row=2, column=1,)

    def confirmOrder(self):
        if self.bOrS == "buy":
            if int(self.userInp.get()) * self.drugPrice > self.master.money:
                messagebox.showerror(title="Error!", message="You do not have enough money to buy that much {}".format(self.drug))

            else:
                self.amount = int(self.userInp.get())
                if messagebox.askokcancel(title="Are you sure?", message="Do you want to buy {} {} for {} dollars?".format(self.amount, self.drug,
                                                                                                                           self.amount*self.drugPrice)):
                    self.destroy()

        elif self.bOrS == "sell":
            if int(self.userInp.get()) > self.master.inv.userInv[self.drugI]:
                messagebox.showerror(title="Error", message="You do not have that much of {}".format(self.drug))

            else:
                self.amount = int(self.userInp.get())
                if messagebox.askokcancel(title="Are you sure?", message="Do you want to sell {} {} for {} dollars?".format(self.amount, self.drug,
                                                                                                                          self.amount*self.drugPrice)):
                    self.destroy()
				
    def isOkay(self, what):
        '''validator for self.userInp, an Entry widget'''
        try:
            int(what)
            return True
        except:
            self.bell()
            return False
		
		
    def destroy(self):
        self.top.destroy()


root = Tk()
root.title("Simulator")
root.resizable(width=False, height=False)
days = int(input("How many days? "))
app = Main(root, days)
app.mainloop()
