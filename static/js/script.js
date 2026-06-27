// Dashboard Chart
const chart = document.getElementById("myChart");

if ($("#barChart").length && dashboardData !== null) {

    new Chart(document.getElementById("barChart"), {

        type: "bar",

        data: {

            labels: [
                "Students",
                "Courses",
                "Attendance",
                "Marks"
            ],

            datasets: [{

                label: "System Statistics",

                data: [

                    dashboardData.students,

                    dashboardData.courses,

                    dashboardData.attendance,

                    dashboardData.marks

                ]

            }]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false

        }

    });

}

if ($("#pieChart").length && dashboardData !== null) {

    new Chart(document.getElementById("pieChart"), {

        type: "doughnut",

        data: {

            labels: [
                "Students",
                "Courses",
                "Attendance",
                "Marks"
            ],

            datasets: [{

                data: [

                    dashboardData.students,

                    dashboardData.courses,

                    dashboardData.attendance,

                    dashboardData.marks

                ]

            }]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false

        }

    });

}

// Students DataTable
$(document).ready(function () {

    if ($("#studentsTable").length) {

        $("#studentsTable").DataTable({

            pageLength: 5,

            lengthMenu: [5, 10, 25, 50],

            ordering: true,

            searching: true,

            responsive: true

        });

    }

});

// Courses DataTable
if ($("#coursesTable").length) {
    $("#coursesTable").DataTable({
        pageLength: 5,
        responsive: true
    });
}

// Enrollment DataTable
if ($("#enrollmentTable").length) {
    $("#enrollmentTable").DataTable({
        pageLength: 5,
        responsive: true
    });
}

// SweetAlert Delete
$(document).on("click", ".delete-course, .delete-enrollment", function () {

    const url = $(this).data("url");

    Swal.fire({
        title: "Are you sure?",
        text: "This action cannot be undone.",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#d33",
        cancelButtonColor: "#0d6efd",
        confirmButtonText: "Yes, Delete"
    }).then((result) => {

        if (result.isConfirmed) {

            window.location.href = url;

        }

    });

});

// Student Course Table
if ($("#studentCourses").length) {

    $("#studentCourses").DataTable({

        pageLength: 5,

        responsive: true

    });

}

if ($("#marksTable").length) {

    $("#marksTable").DataTable({
        pageLength: 5,
        responsive: true
    });

}

$(document).on("click", ".delete-mark", function () {

    const url = $(this).data("url");

    Swal.fire({

        title: "Delete Marks?",

        text: "This action cannot be undone.",

        icon: "warning",

        showCancelButton: true,

        confirmButtonText: "Delete",

        confirmButtonColor: "#dc3545"

    }).then((result) => {

        if (result.isConfirmed) {

            window.location = url;

        }

    });

});

if ($("#studentMarksTable").length) {

    $("#studentMarksTable").DataTable({
        pageLength: 5,
        responsive: true
    });

}

// if ($("#dashboardChart").length) {

//     new Chart(document.getElementById("dashboardChart"), {

//         type: "bar",

//         data: {

//             labels: [

//                 "Students",

//                 "Courses",

//                 "Attendance",

//                 "Marks"

//             ],

//             datasets: [{

//                 label: "System Data",

//                 data: [

//                     Number(document.querySelectorAll(".card h2")[0].innerText),

//                     Number(document.querySelectorAll(".card h2")[1].innerText),

//                     Number(document.querySelectorAll(".card h2")[2].innerText),

//                     Number(document.querySelectorAll(".card h2")[3].innerText)

//                 ]

//             }]

//         },

//         options: {

//             responsive: true,

//             plugins: {

//                 legend: {

//                     display: false

//                 }

//             }

//         }

//     });

// }

if ($("#liveClock").length) {

    setInterval(() => {

        document.getElementById("liveClock").innerHTML =
            new Date().toLocaleString();

    }, 1000);

}

document.querySelectorAll(".card h1").forEach((counter) => {

    const target = Number(counter.innerText);

    if (isNaN(target)) return;

    let count = 0;

    const speed = Math.max(1, Math.ceil(target / 50));

    const update = () => {

        if (count < target) {

            count += speed;

            if (count > target) count = target;

            counter.innerText = count;

            requestAnimationFrame(update);

        }

    };

    update();

});

const darkBtn = document.getElementById("darkModeBtn");

if (darkBtn) {

    darkBtn.onclick = () => {

        document.body.classList.toggle("bg-dark");
        document.body.classList.toggle("text-white");

        document.querySelectorAll(".glass-card").forEach(card => {

            card.classList.toggle("bg-dark");
            card.classList.toggle("text-white");

        });

    };

}

if ($("#analyticsChart").length) {

    new Chart(document.getElementById("analyticsChart"), {

        type: "line",

        data: {

            labels: [

                "Jan",
                "Feb",
                "Mar",
                "Apr",
                "May",
                "Jun"

            ],

            datasets: [{

                label: "Student Activity",

                data: [

                    10,
                    25,
                    18,
                    40,
                    35,
                    dashboardData
                        ? dashboardData.students
                        : 0

                ],

                fill: false,

                tension: 0.4

            }]

        },

        options: {

            responsive: true

        }

    });

}

const todayDate = document.getElementById("todayDate");

if (todayDate) {

    todayDate.innerHTML =
        new Date().toDateString();

}