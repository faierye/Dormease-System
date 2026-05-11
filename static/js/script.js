//ADMIN LOGIN

const loginForm = document.getElementById("loginForm");

if (loginForm) {
    loginForm.addEventListener("submit", function(e) {

        const username = document.querySelector("input[name='username']").value.trim();
        const password = document.querySelector("input[name='password']").value.trim();

        if (username === "" || password === "") {
            e.preventDefault();
            alert("Please fill in all fields!");
        }
    });
}


// LANDING PAGE

function applyNow() {
    window.location.href = "/apply";
}

function goLogin() {
    window.location.href = "/login";
}

// APPLICATION

function toggleFields() {
    const type = document.getElementById("type").value;

    const studentBox = document.getElementById("studentBox");
    const employeeBox = document.getElementById("employeeBox");

    const studentInputs = studentBox.querySelectorAll("input, select");
    const employeeInputs = employeeBox.querySelectorAll("input, select");

    if (type === "student") {
        studentBox.style.display = "block";
        employeeBox.style.display = "none";

        // enable student required
        studentInputs.forEach(input => input.required = true);

        // disable employee required
        employeeInputs.forEach(input => input.required = false);

    } else if (type === "employee") {
        studentBox.style.display = "none";
        employeeBox.style.display = "block";

        // disable student required
        studentInputs.forEach(input => input.required = false);

        // enable employee required
        employeeInputs.forEach(input => input.required = true);
    }
}

// IMAGE PREVIEW (STUDENT + EMPLOYEE)
document.addEventListener("DOMContentLoaded", function () {

    function previewImage(inputId, previewId) {
        const input = document.getElementById(inputId);
        const preview = document.getElementById(previewId);

        if (!input || !preview) return;

        input.addEventListener("change", function () {
            const file = this.files[0];

            if (file) {
                const reader = new FileReader();

                reader.onload = function (e) {
                    preview.src = e.target.result;
                    preview.style.display = "block";
                };

                reader.readAsDataURL(file);
            }
        });
    }

    // call for both
    previewImage("studentInput", "studentPreview");
    previewImage("employeeInput", "employeePreview");

});

function landingPage() {
    window.location.href = "/";
}

//Error and Success
function closeModal() {
    document.getElementById("modal").style.display = "none";
    window.location.href = "/";
}

//DASHBOARD
// TOGGLE SIDEBAR
const menuBtn = document.getElementById("menu-btn");
const sidebar = document.getElementById("sidebar");

if (menuBtn && sidebar) {
    menuBtn.addEventListener("click", () => {
        sidebar.classList.toggle("hide");
    });
}

// SAMPLE CHART

const ctx = document.getElementById('myChart');

if (ctx) {
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Students', 'Employees'],
            datasets: [{
                data: [110, 40],
                backgroundColor: ['#4a69bd', '#f6b93b']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '60%'
        }
    });
}

// SAMPLE ACTIVITY DATA RECENT ACTIVITIES

const activityList = document.getElementById("activityList");

if (activityList) {
    const activities = [
        "New resident registered",
        "Payment received",
        "Room assigned",
        "Application approved"
    ];

    activities.forEach(act => {
        const li = document.createElement("li");
        li.textContent = act;
        activityList.appendChild(li);
    });
}

// PASSWORD TOGGLE - FIXED
document.addEventListener("DOMContentLoaded", function () {

    const passwordInput = document.getElementById("password");
    const togglePassword = document.getElementById("togglePassword");

    if (!passwordInput || !togglePassword) return;

    togglePassword.addEventListener("click", function () {

        const isHidden = passwordInput.type === "password";

        // toggle password visibility
        passwordInput.type = isHidden ? "text" : "password";

        // toggle icon
        togglePassword.classList.toggle("fi-rr-eye");
        togglePassword.classList.toggle("fi-rr-eye-crossed");
    });

});

// Sidebar active toggle
const menuItems = document.querySelectorAll(".menu li");

menuItems.forEach(item => {
    item.addEventListener("click", () => {
        document.querySelector(".active").classList.remove("active");
        item.classList.add("active");
    });
});

// Search filter (basic demo)
const searchInput = document.querySelector(".search-group input");

searchInput.addEventListener("keyup", () => {
    const value = searchInput.value.toLowerCase();
    const cards = document.querySelectorAll(".card");

    cards.forEach(card => {
        card.style.display = card.innerText.toLowerCase().includes(value)
            ? "grid"
            : "none";
    });
});