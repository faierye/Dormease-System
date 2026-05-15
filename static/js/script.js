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

// NOTIFICATION STYLES
(function() {
    const s = document.createElement('style');
    s.textContent = `
        .notif-wrapper { position: relative; display: inline-flex; align-items: center; cursor: pointer; }
        .notif-badge {
            position: absolute;
            top: -6px; right: -8px;
            background: #e53935;
            color: white;
            font-size: 10px;
            font-weight: 700;
            min-width: 16px;
            height: 16px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 0 4px;
            font-family: "Poppins", sans-serif;
            line-height: 1;
        }
        .notif-dropdown {
            display: none;
            position: absolute;
            top: 36px; right: 0;
            width: 320px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.15);
            z-index: 9999;
            overflow: hidden;
        }
        .notif-dropdown.open { display: block; }
        .notif-drop-header {
            padding: 14px 18px;
            background: #3b3b98;
            color: white;
            font-size: 13px;
            font-weight: 700;
            font-family: "Poppins", sans-serif;
        }
        .notif-list { max-height: 320px; overflow-y: auto; }
        .notif-item {
            display: flex;
            flex-direction: column;
            gap: 2px;
            padding: 12px 18px;
            border-bottom: 1px solid #f0f0f0;
            cursor: pointer;
            text-decoration: none;
            transition: background 0.15s;
        }
        .notif-item:hover { background: #f5f5ff; }
        .notif-item:last-child { border-bottom: none; }
        .notif-item-name {
            font-size: 13px;
            font-weight: 600;
            color: #333;
            font-family: "Poppins", sans-serif;
        }
        .notif-item-meta {
            font-size: 11px;
            color: #999;
            font-family: "Poppins", sans-serif;
        }
        .notif-empty {
            padding: 24px 18px;
            text-align: center;
            color: #bbb;
            font-size: 13px;
            font-family: "Poppins", sans-serif;
        }
        .notif-footer {
            padding: 10px 18px;
            text-align: center;
            border-top: 1px solid #f0f0f0;
        }
        .notif-footer a {
            font-size: 12px;
            color: #3b3b98;
            font-weight: 600;
            text-decoration: none;
            font-family: "Poppins", sans-serif;
        }
    `;
    document.head.appendChild(s);
})();

// NOTIFICATION BELL
const notifBell = document.getElementById('notifBell');
if (notifBell) {
    // Build dropdown
    const dropdown = document.createElement('div');
    dropdown.className = 'notif-dropdown';
    dropdown.innerHTML = `
        <div class="notif-drop-header">New Applications</div>
        <div class="notif-list" id="notifList"><div class="notif-empty">Loading...</div></div>
        <div class="notif-footer"><a href="/applications?status=Pending">View all applications →</a></div>
    `;
    notifBell.appendChild(dropdown);

    // Load count + list
    function loadNotifications() {
        fetch('/api/pending_applications')
            .then(r => r.json())
            .then(data => {
                const list = document.getElementById('notifList');
                const apps = data.applications;

                // Update badge
                const existing = notifBell.querySelector('.notif-badge');
                if (existing) existing.remove();
                if (apps.length > 0) {
                    const badge = document.createElement('span');
                    badge.className = 'notif-badge';
                    badge.textContent = apps.length;
                    notifBell.insertBefore(badge, dropdown);
                }

                // Fill list
                if (apps.length === 0) {
                    list.innerHTML = '<div class="notif-empty">No pending applications.</div>';
                } else {
                    list.innerHTML = apps.map(a => `
                        <a class="notif-item" href="/application/${a.id}">
                            <span class="notif-item-name">${a.name}</span>
                            <span class="notif-item-meta">${a.type} &bull; Applied ${a.date}</span>
                        </a>
                    `).join('');
                }
            });
    }

    loadNotifications();

    // Toggle dropdown on click
    notifBell.addEventListener('click', function(e) {
        e.stopPropagation();
        dropdown.classList.toggle('open');
    });

    // Close when clicking outside
    document.addEventListener('click', function() {
        dropdown.classList.remove('open');
    });
}

//DASHBOARD

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
        const activeItem = document.querySelector(".active");
        if (activeItem) activeItem.classList.remove("active");
        item.classList.add("active");
    });
});

// Search filter (basic demo)
const searchInput = document.querySelector(".search-group input");

if (searchInput) {
    searchInput.addEventListener("keyup", () => {
        const value = searchInput.value.toLowerCase();
        const cards = document.querySelectorAll(".card");

        cards.forEach(card => {
            card.style.display = card.innerText.toLowerCase().includes(value)
                ? "grid"
                : "none";
        });
    });
}