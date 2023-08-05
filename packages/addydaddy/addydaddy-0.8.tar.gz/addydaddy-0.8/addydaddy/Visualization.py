from IPython.display import display, HTML

class Color():
    """
        Function to color dataframe
        
        Args: 
            Color(DataFrame,ColorName(Optional))

            ex. Color(df,'red')
        
        Returns: 
            dataframe: colored
    
    """
    
    
    def __init__(self, DataFrame,colorName='lightgrey'):

        

        self.df = DataFrame
        self.colorName=colorName
        self.color()
    
    def color(self):
    
        """Function for blue different color
        
        Args: 
            None
        
        Returns: 
            dataframe: colored
    
        """
        
        self.r=HTML('''
        <style>
            .df tbody tr:nth-child(even) { background-color: '''+self.colorName+'''; }
        </style>
        ''' + self.df.to_html(classes="df"))
                
        display(self.r)
