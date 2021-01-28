class Utility:

    @staticmethod
    def parse_file(filename):
        f = open(filename, 'r')
        lines = f.readlines()
        f.close()

        reservations = []

        for l in lines:
            if l:
                rnum, count = l.split(" ")
                count = int(count.strip())
                reservations.append([rnum, count])
        
        return reservations

    @staticmethod
    def save_to_file(content):
        content.lstrip()
        f = open('out.txt', 'w')
        f.write(content)
        f.close()


    @staticmethod    
    def get_letter(n):
        l = chr(n + 97)
        l = l.upper()
        return l
