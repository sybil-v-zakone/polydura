from loguru import logger

from models.database import Database
from modules.full_warmup import full_warmup

start_message = r"""

                                  ^Y                  
                                 ~&@7                
                      75~:.     !@&~&:       , .      
                      .&&PYY7^.7@@# J#   .^7JPB^      
                       ^@&Y:^?Y&@@P  GBB&@@GP&~       
                        7@@&?  :&@J  G@@&Y.~#^        
                     .:~?&#&@&? !@! B@G~  !&:         
                :75PPY?!^. .:?GG~P!5P~^!YG@@GJ~.      
                .~YG#&&##B#BGPJ?J??J?J5GBBBB##&#B5!.  
                    .^?P&@BJ!^^5G~G^5GJ^. .:!?Y5P57:\  
                       .#?  ^P@#.:@J !&@@#&J~^.       
                      :#7.J&@@#. !@@~  !&@@5          
                     ^&GP@@&BG#. J@@@5?~:?&@7         
                    :BGJ7^..  GG P@@J.:!JY5&@:        
                    .         .&7B@?      .~YJ        
                              ^&@7                   
                                ?!                  
                                                                       
               __    _ __                        __                  
   _______  __/ /_  (_) /  _   __   ____  ____ _/ /______  ____  ___ 
  / ___/ / / / __ \/ / /  | | / /  /_  / / __ `/ //_/ __ \/ __ \/ _ \
 (__  ) /_/ / /_/ / / /   | |/ /    / /_/ /_/ / ,< / /_/ / / / /  __/   
/____/\__, /_.___/_/_/    |___/    /___/\__,_/_/|_|\____/_/ /_/\___/ 
     /____/                                                          

Modules:
1: create_database  | create database
2: warmup_mode      | minter + bridger
3: bridge_mode      | bridger of minted NFTs (in developement)
"""


def main():
    logger.info(start_message)
    module = input("Module: ")
    logger.info(f"Starting module {module}")

    if module == "1":
        Database.create_db()
    elif module == "2":
        full_warmup()
    elif module == "3":
        logger.warning("Bridge mode is currently in developement.")
    else:
        logger.exception("Wrong module selected.")


if __name__ == "__main__":
    main()
