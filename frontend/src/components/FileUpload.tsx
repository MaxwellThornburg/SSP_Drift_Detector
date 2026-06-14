import React, { useCallback, useMemo } from 'react';

interface FileUploadProps {
  onFileSelect: (file: File) => void;
  selectedFile: File | null;
  accept?: string;
  label?: string;
  description?: string;
}

const FileUpload: React.FC<FileUploadProps> = ({
  onFileSelect,
  selectedFile,
  accept = '.md,.txt',
  label = 'File',
  description = 'Drag and drop or click to browse',
}) => {
  const allowedExtensions = useMemo(
    () => accept.split(',').map((ext) => ext.trim().toLowerCase()),
    [accept]
  );

  const isAllowed = useCallback(
    (file: File) =>
      allowedExtensions.some((ext) => file.name.toLowerCase().endsWith(ext)),
    [allowedExtensions]
  );

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      e.stopPropagation();

      const files = e.dataTransfer.files;
      if (files.length > 0 && isAllowed(files[0])) {
        onFileSelect(files[0]);
      }
    },
    [onFileSelect, isAllowed]
  );

  const handleFileInput = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const files = e.target.files;
      if (files && files.length > 0 && isAllowed(files[0])) {
        onFileSelect(files[0]);
      }
      // Reset so the same file can be re-selected after clearing
      e.target.value = '';
    },
    [onFileSelect, isAllowed]
  );

  return (
    <div className="w-full">
      <label className="block text-sm font-medium text-gray-300 mb-2">
        {label}
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
          accept={accept}
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
                {description}
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