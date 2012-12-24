

from pyvalidate import validate, ValidationException

@validate(arg_types=[int, str, str],
          deny_match=['xxx', 'tiktik'],
          requires=['phone'],
          deny='query',
          deny_except='query2',
          types={'phone':str, 'address':str, 'age':int},
          values={'phone':'^\d*$'},
          ignore='age',
          defaults={'address':'nothing'})
def add_person(serial, firstname, lastname, phone=None, address=None, age=None, **kw):
    print 'adding person "%s:%s %s:%s" with serial: %s:%s phone: %s:%s address: %s:%s age:%s:%s' \
            % (firstname, type(firstname),
               lastname, type(lastname),
               serial, type(serial),
               phone,
               type(phone),
               address,
               type(address),
               age,
               type(age))
    
def test(*args, **kwargs):
    try:
        add_person(*args, **kwargs)
    except ValidationException as ex:
        print ex.message

def main():
    test(12, "Vahid", "Mardani", phone="09122451075", address="Tehran")
    test("12", "Vahid", "Mardani", phone='+9122451075', address="Tehran")
    test("12", "Vahid", "Mardani", phone='1')
    test("12", "Vahid", "Mardani", phone='tiktik')
    test("12", "xxx", "Mardani", phone='')
    test("12", "", "Mardani",)
    test("12", "", "Mardani", phone='1', query='123')
    test("12", "", "Mardani", phone='1', query2='123')
    test("12", "", "Mardani", phone='1', age='123')
    
if __name__ == '__main__':
    main()
