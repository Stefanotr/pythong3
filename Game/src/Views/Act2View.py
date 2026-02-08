


from Views.Act1View import ActView





class Act2View:
  
    
    def __new__(cls, screen, player=None, sequence_controller=None):
       
        return ActView.create_act2(screen, player, sequence_controller)


