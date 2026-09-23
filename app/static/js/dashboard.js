document.addEventListener("DOMContentLoaded", () => {

    const dashboard = document.getElementById("dashboard-data");

    if (!dashboard) return;

    const totalBooks = parseInt(dashboard.dataset.totalBooks);
    const issuedBooks = parseInt(dashboard.dataset.issuedBooks);
    const returnedBooks = parseInt(dashboard.dataset.returnedBooks);

    const categoryLabels = JSON.parse(dashboard.dataset.categoryLabels);
    const categoryCounts = JSON.parse(dashboard.dataset.categoryCounts);

    const availableBooks = totalBooks - issuedBooks;

    // ==========================
    // Books Overview
    // ==========================

    new Chart(
        document.getElementById("booksChart"),
        {
            type: "doughnut",

            data: {
                labels: [
                    "Available",
                    "Issued"
                ],

                datasets: [{
                    data: [
                        availableBooks,
                        issuedBooks
                    ],

                    backgroundColor: [
                        "#198754",
                        "#0d6efd"
                    ]
                }]
            },

            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        }
    );

    // ==========================
    // Issue vs Return
    // ==========================

    new Chart(
        document.getElementById("transactionChart"),
        {
            type: "bar",

            data: {
                labels: [
                    "Issued",
                    "Returned"
                ],

                datasets: [{
                    label: "Books",

                    data: [
                        issuedBooks,
                        returnedBooks
                    ],

                    backgroundColor: [
                        "#ffc107",
                        "#20c997"
                    ]
                }]
            },

            options: {
                responsive: true,

                maintainAspectRatio: false,

                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        }
    );

    // ==========================
    // Books by Category
    // ==========================

    new Chart(
        document.getElementById("categoryChart"),
        {
            type: "pie",

            data: {

                labels: categoryLabels,

                datasets: [{

                    data: categoryCounts,

                    backgroundColor: [
                        "#0d6efd",
                        "#198754",
                        "#ffc107",
                        "#dc3545",
                        "#6f42c1",
                        "#fd7e14",
                        "#20c997",
                        "#6610f2"
                    ]

                }]

            },

            options: {

                responsive: true,

                plugins: {

                    legend: {
                        position: "bottom"
                    }

                }

            }

        }
    );

});