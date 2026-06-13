import { useState } from "react";
import FileUpload from "./components/FileUpload";
import RepoInput from "./components/RepoInput";
import ComplianceChart from "./components/ComplianceChart";
import { useApi } from "./hooks/useApi";

declare global {
  interface Window {
    pywebview?: {
      api: {
        close: () => void;
        [key: string]: unknown;
      };
    };
  }
}

interface ComplianceData {
  compliant: number;
  nonCompliant: number;
  notImplemented: number;
  compliancePercentage: number;
}

function App() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [repoUrl, setRepoUrl] = useState("");
  const [analysisResult, setAnalysisResult] = useState<ComplianceData | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const { uploadSSP, analyzeRepo, error } = useApi();

  const handleFileSelect = (file: File) => {
    setSelectedFile(file);
    setAnalysisResult(null);
  };

  const handleRepoChange = (value: string) => {
    setRepoUrl(value);
    setAnalysisResult(null);
  };

  const handleAnalyze = async () => {
    if (!selectedFile || !repoUrl) return;

    setIsAnalyzing(true);
    try {
      await uploadSSP(selectedFile);
      const result = await analyzeRepo(repoUrl);
      setAnalysisResult(result);
    } catch {
      // error is handled by useApi hook
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleClose = () => {
    if (window.pywebview?.api?.close) {
      window.pywebview.api.close();
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 flex flex-col items-center justify-center p-8 relative">
      {/* Brushed metal texture overlay */}
      <div className="fixed inset-0 w-screen h-screen pointer-events-none"
        style={{
          background: `
            repeating-linear-gradient(
              90deg,
              transparent,
              transparent 1px,
              rgba(255,255,255,0.02) 1px,
              rgba(255,255,255,0.02) 2px
            ),
            repeating-linear-gradient(
              0deg,
              transparent,
              transparent 2px,
              rgba(255,255,255,0.01) 2px,
              rgba(255,255,255,0.01) 4px
            ),
            linear-gradient(135deg, #1a1a2e 0%, #16213e 40%, #1a1a2e 60%, #0f3460 100%)
          `
        }}
      />
      
      {/* Title */}
      <h1 className="text-3xl font-bold tracking-widest text-gray-200 mb-2 uppercase relative z-10">
        SSP Drift Detector
      </h1>
      <p className="text-gray-500 text-sm mb-12 tracking-wider relative z-10">
        COMPLIANCE MONITORING SYSTEM
      </p>

      {/* Main Content */}
      <div className="w-full max-w-4xl relative z-10 space-y-6">
        {/* Step 1: Upload SSP */}
        <div className="metal-sheen rounded-lg border border-gray-700 p-8 backdrop-blur-sm">
          <h2 className="text-lg font-semibold text-gray-300 mb-4">1. Upload SSP</h2>
          <FileUpload onFileSelect={handleFileSelect} selectedFile={selectedFile} />
        </div>

        {/* Step 2: Repository Input */}
        {selectedFile && (
          <div className="metal-sheen rounded-lg border border-gray-700 p-8 backdrop-blur-sm">
            <h2 className="text-lg font-semibold text-gray-300 mb-4">2. Analyze Repository</h2>
            <RepoInput value={repoUrl} onChange={handleRepoChange} />

            {repoUrl && (
              <button
                onClick={handleAnalyze}
                disabled={isAnalyzing}
                className="mt-4 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white px-6 py-2 rounded-lg transition"
              >
                {isAnalyzing ? "Analyzing..." : "Run Analysis"}
              </button>
            )}
          </div>
        )}

        {/* Error Display */}
        {error && (
          <p className="text-sm text-red-400 relative z-10">{error}</p>
        )}

        {/* Step 3: Results */}
        {analysisResult && (
          <div className="metal-sheen rounded-lg border border-gray-700 p-8 backdrop-blur-sm">
            <h2 className="text-lg font-semibold text-gray-300 mb-4">3. Results</h2>
            <ComplianceChart data={analysisResult} />
          </div>
        )}
      </div>

      {/* Window controls (since frameless) */}
      <div className="absolute top-4 right-4 flex gap-2 z-20">
        <button 
          onClick={handleClose}
          className="w-3 h-3 rounded-full bg-red-500 hover:bg-red-400 transition-colors"
        />
      </div>
    </div>
  );
}

export default App;