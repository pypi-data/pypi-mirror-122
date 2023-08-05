def int_to_fa(num):
    d = { 0 : 'صفر', 1 : 'يک', 2 : 'دو', 3 : 'سه', 4 : 'چهار', 5 : 'پنج',
        6 : 'شش', 7 : 'هفت', 8 : 'هشت', 9 : 'نه', 10 : 'ده',
        11 : 'يازده', 12 : 'دوازده', 13 : 'سيزده', 14 : 'چهارده',
        15 : 'پانزده', 16 : 'شانزده', 17 : 'هفده', 18 : 'هجده',
        19 : 'نوزده', 20 : 'بيست',
        30 : 'سي', 40 : 'چهل', 50 : 'پنجاه', 60 : 'شصت',
        70 : 'هفتاد', 80 : 'هشتاد', 90 : 'نود'}
    s = { 1 : 'صد ' , 2 : 'دويست ' , 3 : 'سيصد ' , 4 : 'چهارصد ' , 5 : 'پانصد ' , 6 : 'ششصد ' ,
        7 : 'هفتصد ' , 8 : 'هشتصد ' , 9 : 'نهصد '}
    
    k = 1000
    m = k * 1000
    b = m * 1000
    t = b * 1000

    assert(0 <= num)

    if (num < 20):
        return d[num]

    if (num < 100):
        if num % 10 == 0: return d[num]
        else: return d[num // 10 * 10] + ' و ' + d[num % 10]

    if (num < k):
        if num % 100 == 0: return s[num // 100] + ' '
        else: return s[num // 100] + 'و ' + int_to_fa(num % 100)

    if (num < m):
        if num % k == 0: return int_to_fa(num // k) + ' هزار'
        else: return int_to_fa(num // k) + ' هزار و ' + int_to_fa(num % k)

    if (num < b):
        if (num % m) == 0: return int_to_fa(num // m) + ' میلیون'
        else: return int_to_fa(num // m) + ' میلیون و ' + int_to_fa(num % m)

    if (num < t):
        if (num % b) == 0: return int_to_fa(num // b) + ' میلیارد'
        else: return int_to_fa(num // b) + ' میلیارد و ' + int_to_fa(num % b)

    if (num % t == 0): return int_to_fa(num // t) + ' بیلیون'
    else: return int_to_fa(num // t) + ' بیلیون و ' + int_to_fa(num % t)

    raise AssertionError('num is too large: %s' % str(num))


if __name__ == '__main__':
    print(int_to_fa(
        
    ))