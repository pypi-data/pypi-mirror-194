import tkinter as tk


class ui:
    def __init__(self, title: str = "", callback=None) -> None:
        """Makes a new TK window with title as the name

        Args:
            title (str, optional): The name of the window. Defaults to "".
            callback (def, optional): An external class callback
        """
        self.canvas = tk.Tk()
        self.canvas.title(title)

        self.Elements = []  # list of elements (Buttons, labels)
        self.Frames = []  # List of frames
        self.callback = callback
        self.font = ("verdana", 20)
        self.tk = tk  # just in case they need it.

    def FontSettings(self, *, font="verdana", size=20):
        """Changes the font settings

        Args:
            font (str, optional): The font type. Defaults to "verdana".
            size (int, optional): The font size. Defaults to 20.
        """
        self.font = (font, size)

    def CreateFrame(self, row: int = 0, column: int = 0) -> tk.Frame:
        """Creates a new frame

        Args:
            row (int, optional): The row position of the frame. Defaults to 0.
            column (int, optional): The column position of the frame. Defaults to 0.

        Returns:
            tk.Frame: The frame object
        """
        Frame = tk.Frame(self.canvas)
        Frame.grid(row=row, column=column)
        self.Frames.append({"Element": Frame, "row": row, "column": column})

        return Frame

    def CreateImage(self, filePath: str) -> tk.PhotoImage:
        """Create an image object with the file

        Args:
            filePath (str): File to make into an image object

        Returns:
            tk.PhotoImage: The image object
        """
        return tk.PhotoImage(file=filePath)

    def __GetUiElement(self, frame=None) -> tk.Canvas or tk.Frame:
        """Returns the default canvas or frame

        Args:
            frame (_type_, optional): The frame to return. Defaults to None.

        Returns:
            _type_: Frame or canvas
        """
        return self.canvas if frame is None else frame

    def __Callback(self, buttonName: str, **kwargs):
        """Callback function for button press

        Args:
            buttonName (string): The name of the button
        """
        if self.callback is not None:
            return self.callback(**kwargs)

        raise NotImplementedError(
            f"{buttonName} has no designated callback function!")

    def AddButton(
        self,
        text: str = "",
        callback=None,
        row: int = 0,
        column: int = 0,
        *,
        textVar: tk.StringVar = None,
        frame=None,
        sticky: str = "nesw",
        callbackArgs: bool = None,
        rowspan: int = 1,
        columnspan: int = 1,
        image: tk.PhotoImage = None
    ) -> tk.Button:
        """Add a new button to the UI

        Args:
            name (str): the text to display on the button
            callback (function): The callback function on button click
            row (int, optional): The row position of the button. Defaults to 0.
            column (int, optional): The column position of the button. Defaults to 0.
            textVar (tk.StringVar, optional): A string variable. Defaults to None.
            frame (optional): Where to add the element to.
            sticky (str, optional): Whever to make the box stick to a side or not. Defaults to nesw.
            rowspan (int, optional): How many rows it covers. Defaults to 1.
            columnspan (int, optional): How many columns it covers. Defaults to 1.
            callbackArgs (any, optional): Value to send to the function
            image (tk.PhotoImage): An image to add to the button

        Returns:
            tk.Button: The button object
        """

        if callback is None:
            callback = self.__Callback

        Button: tk.Button = None

        def cmd():
            if callbackArgs:
                return callback(callbackArgs)
            return callback()

        Button = tk.Button(
            self.__GetUiElement(frame),
            text=text,
            textvariable=textVar,
            command=cmd,
            font=self.font,
            image=image
        )

        Button.grid(
            row=row,
            column=column,
            sticky=sticky,
            rowspan=rowspan,
            columnspan=columnspan,
        )
        self.Elements.append({"Element": Button, "row": row, "column": column})
        return Button

    def AddLabel(
        self,
        text: str = "",
        row: int = 0,
        column: int = 0,
        *,
        textVar: tk.StringVar = None,
        frame=None,
        sticky: str = "nesw",
        rowspan: int = 1,
        columnspan: int = 1,
        image: tk.PhotoImage = None,
    ) -> tk.Label:
        """Adds a new label to the UI

        Args:
            text (str): The text to display on the label
            row (int, optional): The row position of the label. Defaults to 0.
            column (int, optional): The column position of the label. Defaults to 0.
            textVar (tk.StringVar, optional): A string variable. Defaults to None.
            frame (optional): Where to add the element to.
            sticky (str, optional): Whever to make the box stick to a side or not. Defaults to nesw.
            rowspan (int, optional): How many rows it covers. Defaults to 1.
            columnspan (int, optional): How many columns it covers. Defaults to 1.
            image (tk.PhotoImage, optional): Assaign an image to the ui. Defaults to None

        Returns:
            tk.Label: The label object
        """

        Label = tk.Label(
            self.__GetUiElement(frame),
            text=text,
            textvariable=textVar,
            font=self.font,
            image=image,
        )
        Label.grid(
            row=row,
            column=column,
            sticky=sticky,
            rowspan=rowspan,
            columnspan=columnspan,
        )
        self.Elements.append({"Element": Label, "row": row, "column": column})
        return Label

    def AddTexBox(
        self,
        textVar: tk.StringVar,
        row: int = 0,
        column: int = 0,
        *,
        frame: tk.Frame = None,
        sticky: str = "nesw",
        rowspan: int = 1,
        columnspan: int = 1,
        show: str = "",
    ) -> tk.Entry:
        """Adds a new text box to the UI

        Args:
            textvar (tk.StringVar): The text variable to assign the data to
            row (int, optional): The row position of the label. Defaults to 0.
            column (int, optional): The column position of the label. Defaults to 0.
            frame (tk.Frame, optional): The frame of the textbox. Defaults to None.
            sticky (str, optional): The sides to stick the box to. Defaults to 'nesw'.
            rowspan (int, optional): How many rows it covers. Defaults to 1.
            columnspan (int, optional): How many columns it covers. Defaults to 1.
            show (str, optional): The text to replace the input with. Defaults to ''.

        Returns:
            tk.Text: The textbox object
        """
        textBox = tk.Entry(
            self.__GetUiElement(frame), font=self.font, textvariable=textVar, show=show
        )
        textBox.grid(
            row=row,
            column=column,
            sticky=sticky,
            rowspan=rowspan,
            columnspan=columnspan,
        )
        self.Elements.append(
            {"Element": textBox, "row": row, "column": column})
        return textBox

    def ChangeState(self, Element, state: bool = True, *, row: int = 0, column: int = 0):
        """Make a element visible or invisible

        Args:
            Element (_type_): The element to change the state of
            state (bool, optional): The state to change to. Defaults to True.
            row (int, optional): The row index to place the element. Defaults to 0.
            column (int, optional): The column index to place the element. Defaults to 0.
        """
        if state:
            return Element.grid(row=row, column=column)
        return Element.grid_forget()

    def CreateStringVar(
        self, frame: tk.Frame = None, default: str = ""
    ) -> tk.StringVar:
        """Creates a tk.StringVar object

        Args:
            frame (tk.Frame, optional): The frame to attach to. Defaults to None.
            default (str, optional): The default value in the string var. Defaults to "".

        Returns:
            tk.StringVar: The string var object
        """
        if frame is None:
            frame = self.canvas
        return tk.StringVar(frame, default)
