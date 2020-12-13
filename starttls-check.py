 
import sys
import dns.resolver
import smtplib
import datetime

# Using readline() 
count = 0
print("STARTTLS Support Checker\nReading domains from:",sys.argv[1]) 
  
with open(sys.argv[1]) as fp: 
    while True: 
        count += 1
        line = fp.readline() 
  
        if not line: 
            break
        #print("Line{}: {}".format(count, line.strip()))    
        resolver = dns.resolver.Resolver()
        resolver.timeout = 1
        resolver.lifetime = 1      
        try:
            for x in resolver.resolve(line.strip(), 'MX'):
                resa = line.strip()
                #print('Host', x.exchange, 'has preference', x.preference)     
                resb =str(x.exchange)
                smtp = smtplib.SMTP(timeout=5)
                #smtp.set_debuglevel(2)
                resc = "UNKNOWN"
                try:
                    smtp.connect(str(x.exchange),25)
                    if smtp.has_extn('starttls'):
                       #print("STARTTLS OK")
                       resc = "YES"
                    else:
                       #print("NO STARTTLS")
                       resc = "NO"
                    try:
                        smtp.quit()
                    except smtplib.SMTPServerDisconnected as error:
                        resc = "ERROR"
                        #print("blahh",error) 
                except smtplib.SMTPDataError as e:
                    #print('[-] {0}'.format(str(e[1])))
                    resc = "ERROR - DATA" 
                except smtplib.SMTPServerDisconnected as e:
                    #print('[-] {0}'.format(str(e)))
                    resc = "ERROR - DISCONNECTED"
                except smtplib.SMTPConnectError as e:
                    #print('[-] {0}'.format(str(e[1])))
                    resc = "ERROR - CONNECT"
                except:
                    resc = "ERROR - UNKNOWN"    
                    #print('Error')
                print(datetime.datetime.now(),",", resa,",", resb,",", resc)  
        except:
            resb = "NO MX RECORD"
            print(datetime.datetime.now(),",", line.strip(),",", resb,",",resb) 
        
  
