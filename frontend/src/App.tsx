import { useState } from "react";
import FileUpload from "./components/FileUpload";
import ComplianceChart from "./components/ComplianceChart";

interface ControlResult {
  control_id: string;
  status: "compliant" | "non_compliant" | "indeterminate" | "not_implemented";
  evidence: string[];
  gap_description: string;
}

interface Summary {
  total_controls: number;
  compliant: number;
  non_compliant: number;
  indeterminate?: number;
  not_implemented?: number;
  compliance_percentage: number;
}

interface AnalysisResult {
  summary: Summary;
  drift_detected: boolean;
  results: ControlResult[];
}

function App() {
  const [sspFile, setSspFile] = useState<File | null>(null);
  const [infraFile, setInfraFile] = useState<File | null>(null);
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async () => {
    if (!sspFile || !infraFile) return;

    setIsAnalyzing(true);
    setError(null);
    setAnalysisResult(null);

    const formData = new FormData();
    formData.append("ssp_file", sspFile);
    formData.append("infra_file", infraFile);

    try {
      const response = await fetch("/api/analyze", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        let errorMsg = `Request failed (${response.status})`;
        try {
          const errData = await response.json();
          errorMsg = errData?.detail || errorMsg;
        } catch {
          errorMsg = `Backend unreachable or returned invalid response (${response.status}).`;
        }
        throw new Error(errorMsg);
      }

      const data: AnalysisResult = await response.json();
      setAnalysisResult(data);
    } catch (err: any) {
      console.error("Analysis failed:", err);
      setError(err.message || "Analysis failed");
    } finally {
      setIsAnalyzing(false);
    }
  };

  const chartData = analysisResult
    ? {
        compliant: analysisResult.summary?.compliant || 0,
        nonCompliant: analysisResult.summary?.non_compliant || 0,
        notImplemented: analysisResult.summary?.indeterminate || analysisResult.summary?.not_implemented || 0,
        compliancePercentage: analysisResult.summary?.compliance_percentage || 0,
      }
    : null;

  return (
    // Removed bg-gray-900 and text-white so your index.css gradient shows through
    <div className="min-h-screen text-slate-800">
      <header className="border-b border-slate-300 bg-white/40 backdrop-blur-sm px-6 py-4 shadow-sm">
        <h1 className="text-3xl font-bold text-slate-900 tracking-wide">SSP Drift Detector</h1>
        <p className="text-slate-600 text-sm font-medium">
          Detect compliance drift between your SSP and infrastructure configuration
        </p>
      </header>

      <main className="max-w-4xl mx-auto p-6 space-y-8">
        <section>
          <h2 className="text-xl font-semibold mb-3 text-slate-800">1. Upload SSP</h2>
          <p className="text-slate-600 text-sm mb-4">
            Upload your System Security Plan (Markdown or text).
          </p>
          <FileUpload
            onFileSelect={setSspFile}
            selectedFile={sspFile}
            accept=".md,.txt"
            label="SSP Document"
            description="Markdown or text files only"
          />
        </section>

        <section>
          <h2 className="text-xl font-semibold mb-3 text-slate-800">
            2. Upload Infrastructure Configuration
          </h2>
          <p className="text-slate-600 text-sm mb-4">
            Upload the infrastructure YAML file to evaluate against the SSP.
          </p>
          <FileUpload
            onFileSelect={setInfraFile}
            selectedFile={infraFile}
            accept=".yaml,.yml"
            label="Infrastructure YAML"
            description="YAML files only"
          />
        </section>

        <section>
          <button
            onClick={handleAnalyze}
            disabled={!sspFile || !infraFile || isAnalyzing}
            className={`
              w-full py-3 px-4 rounded-lg font-semibold text-lg tracking-wide
              transition-all duration-200 shadow-md
              ${!sspFile || !infraFile || isAnalyzing
                ? "bg-slate-300 text-slate-500 cursor-not-allowed"
                : "bg-blue-600 hover:bg-blue-700 text-white hover:shadow-lg"
              }
            `}
          >
            {isAnalyzing ? "Analyzing..." : "Analyze Infrastructure"}
          </button>
        </section>

        {error && (
          <section className="rounded-lg border border-red-400 bg-red-100 p-4">
            <p className="text-sm text-red-700 font-medium">{error}</p>
          </section>
        )}

        {analysisResult && (
          <section>
            <h2 className="text-xl font-semibold mb-3 text-slate-800">3. Results</h2>
            
            {chartData && <ComplianceChart data={chartData} />}

            <div className="mt-8">
              <h3 className="text-lg font-semibold mb-6 text-slate-800">
                Control Evaluations ({(analysisResult.results || []).length})
              </h3>
              
              {/* Inline style guarantees the newline/gap between controls regardless of Tailwind caching */}
              <ul style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
                {(analysisResult.results || []).map((item) => {
                  const isPass = item.status === "compliant";
                  const isFail = item.status === "non_compliant";
                  
                  // Explicit colors: Green, Red, Gray
                  const badgeColor = isPass ? "#16a34a" : isFail ? "#dc2626" : "#6b7280";
                  const statusText = isPass ? "PASS" : isFail ? "FAIL" : "INDETERMINATE";
                  
                  const cardBg = isPass ? "rgba(22, 163, 74, 0.08)" : isFail ? "rgba(220, 38, 38, 0.08)" : "rgba(255, 255, 255, 0.6)";
                  const cardBorder = isPass ? "1px solid rgba(22, 163, 74, 0.3)" : isFail ? "1px solid rgba(220, 38, 38, 0.3)" : "1px solid rgba(148, 163, 184, 0.6)";

                  return (
                    <li
                      key={item.control_id}
                      style={{
                        background: cardBg,
                        border: cardBorder,
                        borderRadius: '12px',
                        padding: '24px',
                        boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.05)'
                      }}
                    >
                      {/* Inline style guarantees the space between the name and the badge */}
                      <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '12px' }}>
                        <span style={{ fontFamily: 'monospace', fontSize: '18px', fontWeight: 'bold', color: '#0f172a' }}>
                          {item.control_id}
                        </span>
                        <span style={{ 
                          fontSize: '12px', 
                          fontWeight: 'bold', 
                          textTransform: 'uppercase', 
                          letterSpacing: '1px', 
                          padding: '4px 12px', 
                          borderRadius: '9999px', 
                          color: 'white',
                          backgroundColor: badgeColor
                        }}>
                          {statusText}
                        </span>
                      </div>

                      {item.evidence && item.evidence.length > 0 && (
                        <div style={{ marginTop: '12px' }}>
                          <p style={{ fontSize: '14px', fontWeight: '600', color: '#334155', marginBottom: '4px' }}>
                            Evidence:
                          </p>
                          <ul style={{ listStyleType: 'disc', paddingLeft: '20px', fontSize: '14px', color: '#475569' }}>
                            {item.evidence.map((ev, i) => (
                              <li key={i} style={{ marginBottom: '4px' }}>{ev}</li>
                            ))}
                          </ul>
                        </div>
                      )}

                      {item.gap_description && item.status !== "compliant" && (
                        <div style={{ marginTop: '12px' }}>
                          <p style={{ fontSize: '14px', fontWeight: '600', color: '#334155', marginBottom: '4px' }}>
                            {item.status === "non_compliant" ? "Gaps:" : "Notes:"}
                          </p>
                          <p style={{ fontSize: '14px', color: '#475569' }}>
                            {item.gap_description}
                          </p>
                        </div>
                      )}
                    </li>
                  );
                })}
              </ul>
            </div>
          </section>
        )}
      </main>
    </div>
  );
}

export default App;