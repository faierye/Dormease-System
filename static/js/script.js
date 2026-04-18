document.getElementById("loginForm").addEventListener("submit", function(e) {

    const username = document.querySelector("input[name='username']").value.trim();
    const password = document.querySelector("input[name='password']").value.trim();

    if (username === "" || password === "") {
        e.preventDefault();
        alert("Please fill in all fields!");
    }
});


function applyNow() {
    window.location.href = "/application";
}

function goLogin() {
    window.location.href = "/login";
}