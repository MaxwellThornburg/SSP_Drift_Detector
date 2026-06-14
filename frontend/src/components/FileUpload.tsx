import React, { useCallback } from 'react';

interface FileUploadProps {
  onFileSelect: (file: File) => void;
  selectedFile: File | null;
}

const FileUpload: React.FC<FileUploadProps> = ({ onFileSelect, selectedFile }) => {
  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();

    const files = e.dataTransfer.files;
    if (files.length > 0) {
      const file = files[0];
      if (file.name.endsWith('.md') || file.name.endsWith('.txt')) {
        onFileSelect(file);
      }
    }
  }, [onFileSelect]);

  const handleFileInput = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      onFileSelect(files[0]);
    }
  }, [onFileSelect]);

  return (
    <div className="w-full">
      <label className="block text-sm font-medium text-gray-300 mb-2">
        SSP
      </label>
      <div
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        className={`
          relative border-2 border-dashed rounded-lg p-6
          transition-colors duration-200
          ${selectedFile
            ? 'border-green-500 bg-green-500/10'
            : 'border-gray-600 hover:border-gray-500 bg-gray-800/50'
          }
        `}
      >
        <input
          type="file"
          accept=".md,.txt"
          onChange={handleFileInput}
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
        />
        <div className="text-center">
          {!selectedFile ? (
            <>
              <p className="mt-2 text-sm text-gray-400">
                <span className="font-medium text-blue-400">Click to upload</span> or drag and drop
              </p>
              <p className="mt-1 text-xs text-gray-500">
                Markdown or text files only
              </p>
            </>
          ) : (
            <>
              <p className="mt-2 text-sm text-green-400 font-medium">
                {selectedFile.name}
              </p>
              <p className="mt-1 text-xs text-gray-500">
                {(selectedFile.size / 1024).toFixed(1)} KB
              </p>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default FileUpload;