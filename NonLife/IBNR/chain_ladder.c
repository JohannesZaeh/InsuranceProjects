#include <stdio.h>
#include <stdlib.h>



// Function to compute the cumulative claims
void computeCumulativeClaims(int rows, int cols, double claims[rows][cols], double cumulative_claims[rows][cols]){
    double sum;

    for (int i = 0; i < rows; i++){
        for (int j = 0; j < cols; j++) {
            if (claims[i][j] != -1){
                sum = 0;
                for (int k = 0; k < j + 1; k++){
                    sum += claims[i][k];
                }
                cumulative_claims[i][j] = sum;
                
            }
            else {
                cumulative_claims[i][j] = -1;
            }
            
        }
    }
}


// Function to calculate development factors
void calculateDevelopmentFactors(int rows, int cols, double cumulative_claims[rows][cols], double factors[cols-1]) {
    for (int j = 0; j < cols - 1; j++) {
        
        double numerator = 0.0;
        double denominator = 0.0;
        for (int i = 0; i < rows; i++) {
            if (cumulative_claims[i][j + 1] != -1) {
                numerator += cumulative_claims[i][j + 1];
                denominator += cumulative_claims[i][j];
            }
        }
        factors[j] = numerator / denominator;
    }
}

// Function to project the cumulative claims
void projectCumulativeClaims(int rows, int cols, double cumulative_claims[rows][cols], double factors[cols-1]){
    for (int i = 0; i < rows; i++){
        for (int j = 0; j < cols; j++){
            if (cumulative_claims[i][j] == -1){
                cumulative_claims[i][j] = cumulative_claims[i][j-1] * factors[j-1];
            }

        }
    }


} 

// Function to fill missing claims using development factors
void fillMissingClaims(int rows, int cols, double claims[rows][cols], double cumulative_claims[rows][cols], double factors[cols-1]) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            if (claims[i][j] == -1) {
                claims[i][j] = cumulative_claims[i][j] - cumulative_claims[i][j-1];

                
            }
        }
    }
}

// Function to write the claims matrix with brackets for reserves to a file
void writeClaimsWithReservesToFile(int rows, int cols, double claims[rows][cols], const char *filename) {
    FILE *file = fopen(filename, "w");
    if (file == NULL) {
        perror("Error opening output file");
        exit(EXIT_FAILURE);
    }

    //write header row
    fprintf(file, "0");
    fprintf(file, "\t");
    for (int j = 0; j < cols; j++){
        fprintf(file, "%d", j);
        fprintf(file, "\t");
    }
    fprintf(file, "\n");

    for (int i = 0; i < rows; i++) {

        fprintf(file, "%d", i);
        fprintf(file, "\t");

        for (int j = 0; j < cols; j++) {
            if (i + j > rows - 1) {
                fprintf(file, "*%.2f", claims[i][j]);
            } else {
                fprintf(file, "%.2f", claims[i][j]);
            }
            if (j < cols - 1) {
                fprintf(file, "\t");
            }
        }
        if (i < rows - 1){
            fprintf(file, "\n");
        }
    }
    fclose(file);
}

// Main function
int main() {
    FILE *file = fopen("claims.txt", "r");
    if (file == NULL) {
        perror("Error opening file");
        return EXIT_FAILURE;
    }

    // Determine the number of columns by reading the first line
    int cols = 0;
    char ch;
    while ((ch = fgetc(file)) != '\n') {
        if (ch == '\t') {
            cols++;
        }
    }

    // Determine the number of rows by counting lines
    int rows = 1;
    while ((ch = fgetc(file)) != EOF) {
        if (ch == '\n') {
            rows++;
        }
    }

    // Reset the file pointer to the beginning of the file
    rewind(file);

    // Skip the first line (header), and the index on the year in the first column.
    while ((ch = fgetc(file)) != '\n');
    fseek(file, 1, SEEK_CUR);

    // Read the claims data
    double claims[rows][cols];
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            if (fscanf(file, "%lf", &claims[i][j]) != 1) {
                claims[i][j] = -1;
            }
        }
        //move file pointer to skip the first column
        if (i < 10-1) {
            fseek(file, 3, SEEK_CUR);
        } else if (i >= 10-1 && i < 100-1) {
            fseek(file, 4, SEEK_CUR);
        } else if (i >= 100-1 && i < 1000-1) {
            fseek(file, 5, SEEK_CUR);
        } else if (i >= 1000-1 && i < 10000-1) {
            fseek(file, 6, SEEK_CUR);
        } else if (i >= 10000-1 && i < 100000-1) {
            fseek(file, 7, SEEK_CUR);
        } else if (i >= 100000-1 && i < 1000000-1) {
            fseek(file, 8, SEEK_CUR);
        } else {
            printf("Too many input rows\n");
            return 0;
        }
        
    }
    fclose(file);
    
    double cumulative_claims[rows][cols];
    computeCumulativeClaims(rows, cols, claims, cumulative_claims);

    double factors[cols - 1];
    calculateDevelopmentFactors(rows, cols, cumulative_claims, factors);

    projectCumulativeClaims(rows, cols, cumulative_claims, factors);
    fillMissingClaims(rows, cols, claims, cumulative_claims, factors);

    writeClaimsWithReservesToFile(rows, cols, claims, "claims_with_reserves.txt");
    
    return 0;
}
