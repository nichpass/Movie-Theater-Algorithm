from utility import Utility

class MovieSolver:

    def __init__(self, filename):

        self.BUFFER_SIZE = 3
        self.LAST_COLUMN = 19
        self.NUM_COLUMNS = 20
        self.NUM_ROWS = 10
        self.CAPACITY = self.NUM_ROWS * self.NUM_COLUMNS

        self.seats  = [['.' for x in range(self.NUM_COLUMNS)] for y in range(self.NUM_ROWS)]
        self.unused_seats_per_row = [self.NUM_COLUMNS] * self.NUM_ROWS

        self.seats_used = 0
        self.active_row = 9
        self.reservations = Utility.parse_file(filename)
        self.num_res = len(self.reservations)
        self.res_out = {}


    def fill_seats(self):
        res_num = 0
        while res_num < self.num_res:
            res, count = self.reservations[res_num]

            if self.capacity_reached(count):
                print("Capacity reached : current reservation cancelled.")
                self.res_out[res] = "Cancelled"
                break

            # when a group is larger than any contiguous block of available seats, we split it into two associated groups
            if self.need_to_split_group(count):
                self.split_group(count, res_num, res)
                continue
            
            self.assign_group(count, res_num, res)

            self.seats_used += count
            res_num += 1


    def capacity_reached(self, group_size):
        return group_size + self.seats_used > self.CAPACITY


    def need_to_split_group(self, group_size):
        return group_size > self.NUM_COLUMNS or group_size > self.get_largest_block()


    def get_largest_block(self):
        best = 0
        for i in range(len(self.seats)):
            cur = self.get_largest_block_in_row(i)
            best = max(best, cur)
        return best


    def get_largest_block_in_row(self, ri):
        row = self.seats[ri]
        best, count, p = 0, 0, 0
        for i in range(len(row)):
            if row[i] == '.':
                if count == 0:
                    p = i
                count += 1
            elif row[i] == '0':
                count = 0

            best = max(best, count)
        return best
            

    def split_group(self, count, res_num, res):
        group1 = count // 2
        group2 = count - group1
        self.reservations[res_num][1] = group1
        self.reservations.insert(res_num, [res, group2])
        self.num_res += 1
            

    def assign_group(self, group_size, res_num, res):
        if res_num < 5:
            self.fill_center(group_size, res_num, res)
        elif res_num > 14:
            self.fill_any(group_size, res)
        elif res_num % 2 == 1:               
            self.fill_left(group_size, res_num, res)
        elif res_num % 2 == 0:              
            self.fill_right(group_size, res)


    def fill_center(self, group_size, res_num, res):
        left = 10 - (group_size // 2)
        right = left + group_size
        self.active_row = 9 - 2 * res_num 
        self.assign_seats(self.active_row, left, right, res)


    def fill_left(self, group_size, res_num, res):
        if res_num == 5:
            self.active_row = 8
        else:
            self.active_row = self.active_row - 2 

        if self.can_fit_on_left(group_size, self.active_row):
            left = 0
            right = left + group_size
            self.assign_seats(self.active_row, left, right, res)
        else:
            self.fill_any(group_size, res)


    def can_fit_on_left(self, group_size, ri):
        count = 0
        p = 0
        
        while p < self.NUM_COLUMNS and self.seats[ri][p] == '.':
            count += 1
            p += 1
        
        return count >= group_size + self.BUFFER_SIZE


    def fill_right(self, group_size, res):
        if self.can_fit_on_right(group_size, self.active_row):
            right = self.LAST_COLUMN
            left = right - group_size
            self.assign_seats(self.active_row, left, right, res)
        else:
            self.fill_any(group_size, res)


    def can_fit_on_right(self, group_size, ri):
        count = 0
        p = self.LAST_COLUMN
        while p >= 0 and self.seats[ri][p] == '.':
            count += 1
            p -= 1
        
        return count >= group_size + self.BUFFER_SIZE


    def fill_any(self, group_size, res):
        self.active_row += 1
        left, right, row = self.search_for_safe_seats(group_size)
        if left == None:
            left, right, row = self.search_for_unsafe_seats(group_size)

        self.assign_seats(row, left, right, res)


    def search_for_safe_seats(self, group_size):
        for i in range(9, -1, -1):
            left, right = self.get_open_safe_seat_block(self.seats[i], group_size)
            if not left == None:
                return left, right, i
        return None, None, None


    def search_for_unsafe_seats(self, group_size):
        for i in range(9, -1, -1):
            left, right = self.get_open_unsafe_seat_block(self.seats[i], group_size)
            if not left == None:
                return left, right, i
        return None, None, None


    def get_open_safe_seat_block(self, row, group_size):
        count = 0
        p = 0
        for i in range(len(row)):
            if row[i] == '.':
                if count == 0:
                    p = i
                count += 1
            elif row[i] == '0':
                count = 0

            # the 3 cases here account for the lack of a side buffer needed on edges
            left_free = (count == group_size + self.BUFFER_SIZE and p == 0)
            right_free = (count == group_size + self.BUFFER_SIZE and p + count  == len(row) - 1)
            center_free = (count == group_size + 6)

            if left_free:
                return p, p + group_size
            elif right_free:
                return self.LAST_COLUMN - group_size, self.LAST_COLUMN
            elif center_free:
                return p + self.BUFFER_SIZE, p + self.BUFFER_SIZE + group_size
        return None, None


    def get_open_unsafe_seat_block(self, row, group_size):
        count = 0
        p = 0
        for i in range(len(row)):
            if row[i] == '.':
                if count == 0:
                    p = i
                count += 1
            elif row[i] == '0':
                count = 0

            if count == group_size:
                return p, p + group_size

        return None, None

    def assign_seats(self, row, left, right, res):
        if max(self.seats[row][left:right]) == '0':
            self.displaySeating()
            print("Attempted to assign seat(s) that were already reserved. Error in code")
            sys.exit(1)

        l = Utility.get_letter(row)

        for i in range(left, right):
            self.seats[row][i] = '0'

            self.res_out[res] = self.res_out.get(res, [])
            self.res_out[res].append(l + str(i))


    def displaySeating(self):
        out = ""
        for r in self.seats:
            out += str(r) + "\n"
        print(out)


    def generate_output(self):
        self.file_out = ""
        for k, arr in self.res_out.items():
            line = "\n" + k + " "
            
            if arr == "Cancelled":
                line += arr
            else:

                for v in arr:
                    line += v + ','
            
            self.file_out += line

        Utility.save_to_file(self.file_out)

