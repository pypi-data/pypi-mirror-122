class Shell():
    '''
		log/print your status and messages on shell or terminal in a
		standardized yet customizable format.

		base is a string to indicate application name
            --<base> $ message > value
	'''
    def __init__(self, base):
        if type(base) != str:
            raise ValueError("base must be a string")
        self.base = '--<{}> $ '.format(str(base))
        self.end = '> '

    def message(self, message, value=''):
        '''
        prints the message and value with the base.

            --<base> $ message > value
        
        '''


        if type(message) != str:
            raise ValueError("message must be a string")
        else:
            shell_str = self.base + message
            if len(shell_str) < 30:
                white_sp = ' ' * (30-len(shell_str))
            else:
                white_sp = ' '

            if value == '':
                end = value
            else:
                end = self.end

            shell_str += white_sp + end + str(value)
            print(shell_str)

