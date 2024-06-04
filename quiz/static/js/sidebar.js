document.addEventListener('DOMContentLoaded', function() {
    var userTypeElem = document.getElementById('user-type');
    var usernameElem = document.getElementById('username');
    var createQuizLink = document.getElementById('create-quiz-link');
    var logoutLink = document.getElementById('logout-link');

   
    var user = {
        userType: user.user_type, 
        username: user.username
    };

   
    userTypeElem.textContent = "User Type: " + user.userType;
    usernameElem.textContent = "Username: " + user.username;

    if (user.userType !== 'teacher') {
        createQuizLink.style.display = 'none';
    }

 
    logoutLink.addEventListener('click', function(event) {
        event.preventDefault();
       
        console.log('Logging out...');
    });
});
