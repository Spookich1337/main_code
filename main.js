function levenshtain(str1, str2) {
    // Константные значения
    const rep = 1, ins = 1, del = 1;
    const m = str1.length;
    const n = str2.length;
    
    // Создание двумерного массива 
    const dp = Array.from({ length: m + 1 }, () => new Array(n + 1));
    
    // Инициализация базовых значений
    for (let i = 0; i <= m; i++) {
        dp[i][0] = i * del;
    }
    for (let j = 0; j <= n; j++) {
        dp[0][j] = j * ins;
    }
    
    // Заполнение матрицы
    for (let i = 1; i <= m; i++) {
        for (let j = 1; j <= n; j++) {
            if (str1[i - 1] === str2[j - 1]) {
                dp[i][j] = dp[i - 1][j - 1];
            } else {
                const replaceCost = dp[i - 1][j - 1] + rep;
                const insertCost = dp[i][j - 1] + ins;
                const deleteCost = dp[i - 1][j] + del;
                dp[i][j] = Math.min(replaceCost, insertCost, deleteCost);
            }
        }
    }
    // Возвращения растояния Левенштейна
    return dp[m][n];
}

// Пример использования
const args = process.argv.slice(2);
if (args.length == 2) {
    const str1 = args[0];
    const str2 = args[1];
    const distance = levenshtain(str1, str2);
    console.log(distance);
} else {
    console.log("error");
}