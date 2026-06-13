import { useState } from "react";
import FileUpload from "./components/FileUpload";
import RepoInput from "./components/RepoInput";
import ComplianceChart from "./components/ComplianceChart";
import { useApi } from "./hooks/useApi";

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

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <header className="border-b border-gray-700 px-6 py-4">
        <h1 className="text-2xl font-bold">SSP Drift Detector</h1>
        <p className="text-gray-400 text-sm">
          Detect compliance drift between your SSP and actual code
        </p>
      </header>

      <main className="max-w-4xl mx-auto p-6 space-y-8">
        <section>
          <h2 className="text-xl font-semibold mb-3">1. Upload SSP</h2>
          <FileUpload onFileSelect={handleFileSelect} selectedFile={selectedFile} />
        </section>

        {selectedFile && (
          <section>
            <h2 className="text-xl font-semibold mb-3">
              2. Analyze Repository
            </h2>
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
          </section>
        )}

        {error && (
          <p className="text-sm text-red-400">{error}</p>
        )}

        {analysisResult && (
          <section>
            <h2 className="text-xl font-semibold mb-3">3. Results</h2>
            <ComplianceChart data={analysisResult} />
          </section>
        )}
      </main>
    </div>
  );
}

export default App;