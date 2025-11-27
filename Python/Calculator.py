import tkinter as tk

# region VALIDATION
def ValidateInteger(value):
    value = UnFormatInteger(value)
    return value.isdigit() or value == ""
#endregion

# region PROCESSES
def FormatInteger(value, isDiscount):
    return f"{int(value):,}" if isDiscount else f"{int(value):,.2f}"

def UnFormatInteger(value):
    value = value.replace(",", "").replace("%", "")
    
    if "." in value:
        value = value.split(".", 1)[0]
        
    return value

def CalculateCursorPosition(prevPosition, newValue, oldValue):
    commasBeforeCursor = newValue[:prevPosition].count(",")
    prevCommasBeforeCursor = oldValue[:prevPosition].count(",")

    offset = commasBeforeCursor - prevCommasBeforeCursor
    return prevPosition + offset

def CalculateResult(price, discount):
    price = UnFormatInteger(price)
    discount = UnFormatInteger(discount)
    return (100 - int(discount))/100 * int(price)
# endregion

# region EVENTS
def OnPriceChanged(event):
    entry = event.widget
    cursorPosition = entry.index(tk.INSERT)
    rawText = txtPrice.get()
    integerValue = UnFormatInteger(rawText)

    if integerValue.isdigit():
        formatted = FormatInteger(integerValue, False)
        txtPrice.set(formatted)

        newPosition = CalculateCursorPosition(cursorPosition, formatted, rawText)
        entry.icursor(newPosition)
        
def OnDiscountChanged(event):
    entry = event.widget
    cursorPosition = entry.index(tk.INSERT)
    rawText = txtDiscount.get()
    integerValue = UnFormatInteger(rawText)

    if integerValue.isdigit():
        formatted = FormatInteger(integerValue, True)
        txtDiscount.set(formatted)

        newPosition = CalculateCursorPosition(cursorPosition, formatted, rawText)
        entry.icursor(cursorPosition)

def UpdateResult():
    result = CalculateResult(txtPrice.get(), txtDiscount.get())
    result = FormatInteger(result, False)
    lblResult.set(result if result != "" else "-")
# endregion

# region FORM
def InitForm():
    form = tk.Tk()
    form.title("Discount Calculator")
    form.geometry("400x250")
    container = tk.Frame(form)
    container.pack(expand=True)

    container.grid_columnconfigure(0, weight=1)
    container.grid_columnconfigure(1, weight=1)

    validateCommand = (container.register(ValidateInteger), "%P")

    # region PRICE
    global txtPrice
    tk.Label(container, text="Price").grid(row=0, column=0)
    txtPrice = tk.StringVar()
    boxPrice = tk.Entry(container, textvariable=txtPrice, validate="key", validatecommand=validateCommand)
    boxPrice.grid(row=1, column=0)
    boxPrice.bind("<KeyRelease>", OnPriceChanged)
    # endregion
    
    # region DISCOUNT
    global txtDiscount
    tk.Label(container, text="Discount").grid(row=2, column=0)
    txtDiscount = tk.StringVar()
    boxDiscount = tk.Entry(container, textvariable=txtDiscount, validate="key", validatecommand=validateCommand)
    boxDiscount.grid(row=3, column=0)
    boxDiscount.bind("<KeyRelease>", OnDiscountChanged)
    # endregion
    
    # region RESULT
    global lblResult
    tk.Label(container, text="Result:").grid(row=4, column=0)
    lblResult = tk.StringVar()
    tk.Label(container, textvariable=lblResult, relief="sunken", width=15).grid(row=5, column=0)
    # endregion
    
    tk.Button(container, text="Calculate", command=UpdateResult).grid(row=6, column=0, pady=10)

    return form

window = InitForm()
window.mainloop()
# endregion