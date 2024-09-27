import { GenericDrawer } from './GenericDrawer.js';

export class ProfileDrawer extends GenericDrawer {
    constructor(params) {
        super(params);

        this.boundHandleDrawerOpened = this.handleDrawerOpened.bind(this);
        this.boundInitGameOutcomesChart = this.initGameOutcomesChart.bind(this);
        this.chart = null;
        this.noGamesMessage = null;
    }

    async handleDrawerOpened(e) {
        this.initGameOutcomesChart();
    }

    async initComponent() {
        document.addEventListener('drawer-opened', this.boundHandleDrawerOpened);
        document.addEventListener('drawer-opened', this.boundInitGameOutcomesChart);
    }

    destroy() {
        super.destroy();
        document.removeEventListener('drawer-opened', this.boundHandleDrawerOpened);
        document.removeEventListener('drawer-opened', this.boundInitGameOutcomesChart);
        if (this.chart) {
            this.chart.destroy();
        }
    }

    initGameOutcomesChart() {
        const gameOutcomesCanvas = this.element.querySelector('#gameOutcomesChart');

        if (gameOutcomesCanvas) {
            const gameOutcomesCtx = gameOutcomesCanvas.getContext('2d');

            // Assume wins and losses are passed as data attributes
            const wins = Number(gameOutcomesCanvas.dataset.wins || 0);
            const losses = Number(gameOutcomesCanvas.dataset.losses || 0);
            const totalGames = wins + losses;

            if (totalGames > 0) {
                const gameOutcomes = [
                    { name: "Wins", value: wins },
                    { name: "Losses", value: losses },
                ];

                // Destroy the existing chart if it exists
                if (this.chart) {
                    this.chart.destroy();
                }

                // Create a new chart
                this.chart = new Chart(gameOutcomesCtx, {
                    type: 'pie',
                    data: {
                        labels: gameOutcomes.map(outcome => outcome.name),
                        datasets: [{
                            data: gameOutcomes.map(outcome => outcome.value),
                            backgroundColor: ['#0A8F17', '#990C0C'],
                        }],
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: {
                                position: 'bottom',
                            },
                            title: {
                                display: true,
                                text: 'Game Outcomes'
                            }
                        }
                    }
                });
                gameOutcomesCanvas.style.display = 'block';

                if (this.noGamesMessage) {
                    this.noGamesMessage.remove();
                    this.noGamesMessage = null;
                }
            } else {
                gameOutcomesCanvas.style.display = 'none';

                if (!this.noGamesMessage) {
                    this.noGamesMessage = document.createElement('p');
                    this.noGamesMessage.className = 'no-games-message';
                    this.noGamesMessage.textContent = "No games played yet.";
                    gameOutcomesCanvas.parentNode.appendChild(this.noGamesMessage);
                }
            }
        }
    }
}