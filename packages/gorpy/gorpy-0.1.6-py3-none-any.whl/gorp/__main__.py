from .readfiles import *
 
 
def main():
    with GorpSession() as session:
        args = sys.argv
        prompt = True
        if len(args) > 1: #first arg is always path to the module's file
            query = ' '.join(args[1:])
            session.receive_query(query)
            prompt = False
        if prompt:
            # print(helpstring)
            while True:
                query = input("gorp> ").strip()
                if query in ['e','q','exit','quit','quit()','exit()']:
                    print("\nGoodbye!")
                    break
                session.receive_query(query)
                # print()
                del query
        return None

    
if __name__ == '__main__':
    main()