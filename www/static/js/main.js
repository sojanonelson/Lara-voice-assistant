document.addEventListener('DOMContentLoaded', (event) => {
    function fetchUserData() {
        eel.fetch_user_data("Name")(function(result) {
            document.getElementById("user-name").innerText = result;
        });
    }

    function playStartSound() {
        eel.start_sound()(function() {
            console.log("Start sound played successfully");
        });
    }

    fetchUserData();
    
    
});

console.log("hello");
