from user import User
from db_manager import db_session

def main():
    u = User(db_session, "USERNAME", "PASS", "EMAIL", "SOME BIO")
    print(u)

    u2 = User(db_session, "USERNAME2", "PASS2", "EMAIL2", "SOME BIO2")
    print(u2)

    u.send_friend_request(db_session, u2)

    print("U SENT: ", u.get_friend_requests_sent(db_session))
    print("U SENT: ", u.get_friends(db_session))
    print("U2 GOT: ", u2.get_friend_requests(db_session))
    print("U2 GOT: ", u2.get_friends(db_session))

    u2.reject_friend_request(db_session, u)
    print("U2 REJECTED U: ", u2.get_friend_requests(db_session))
    print("U2 REJECTED U: ", u.get_friend_requests_sent(db_session))
    print("U2 REJECTED U: ", u.get_friends(db_session))
    print("U2 REJECTED U: ", u2.get_friends(db_session))

    u.send_friend_request(db_session, u2)
    u2.accept_friend_request(db_session, u)

    print("U2 ACCEPTED U: ", u2.get_friends(db_session))
    print("U2 ACCEPTED U: ", u.get_friends(db_session))

    u.remove_friend(db_session, u2)

    print("U REMOVED U2: ", u.get_friends(db_session))
    print("U REMOVED U2: ", u2.get_friends(db_session))

if __name__ == "__main__":
    main()