#include <iostream>
#include <vector>
#include <cmath>
#include "TCanvas.h"
#include "TGraph.h"
#include "TAxis.h"
#include "TLegend.h"

// Function to represent stachiwCycle
double stachiwCycle1(double t) {
    double room_temp = 27;
    double timeRegion1 = (140.0 - room_temp)/10.0;
    double timeRegion2 = timeRegion1 + 50;  // Hold for 50 hours at 140degC
    double timeRegion3 = timeRegion2 + (140.0 - 110.0)/std::abs(1.222);
    double timeRegion4 = timeRegion3 + 25;   // Hold for 25 hours at 110degC
    double timeRegion5 = timeRegion4 + (110.0 - room_temp)/std::abs(1.944);

    if (0 <= t && t <= timeRegion1) {
        return 10.0* t + room_temp;
    } else if (timeRegion1 < t && t <= timeRegion2) {
        return 140.0;
    } else if (timeRegion2 < t && t <= timeRegion3) {
        return 140.0 + -1*1.222*(t - timeRegion2);
    } else if (timeRegion3 < t && t <= timeRegion4) {
        return 110.0;
    } else if (timeRegion4 <= t && t < timeRegion5) {
        return 110.0 + -1*1.944*(t - timeRegion4);
    } else {
        return 0;  // Return 0 if t is out of bounds
    }
}

void plotStachiwCycle() {
    // Time vectors for the different cycles
    int endTime = 153; // total time
    int nPoints = endTime*100;
    std::vector<double> time_stachiwCycle1(nPoints);
    std::vector<double> temperature_stachiwCycle1(nPoints);
    
    for (int i = 0; i < nPoints; ++i) {
        time_stachiwCycle1[i] = i*0.01;  // Fill the time values
        temperature_stachiwCycle1[i] = stachiwCycle1(time_stachiwCycle1[i]);
    }

    // Create canvas
    TCanvas *c1 = new TCanvas("c1", "Annealing Cycle", 800, 600);

    // Create a graph
    TGraph *gr1 = new TGraph(nPoints, &time_stachiwCycle1[0], &temperature_stachiwCycle1[0]);
    gr1->SetLineColor(kGray+1);// Line color
    gr1->SetLineWidth(2);  // Line width
    gr1->SetLineStyle(2);  // Dashed line
    gr1->SetTitle("Annealing Cycle, raw single-layer");
    gr1->GetXaxis()->SetTitle("Hours");
    gr1->GetYaxis()->SetTitle("Temperature (^{#circ}C,");

    // Draw graph
    gr1->Draw("AL");  // "A" for axes, "L" for line

    // Grid and legend
    c1->SetGridx();
    c1->SetGridy();
    TLegend *legend = new TLegend(0.6, 0.7, 0.9, 0.9);
    legend->AddEntry(gr1, "Annealing cycle 1, raw single-layer", "l");
    legend->Draw();

    // Show plot
    c1->Update();
    c1->Draw();
}
