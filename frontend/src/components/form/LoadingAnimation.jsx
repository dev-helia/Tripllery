export default function LoadingAnimation() {
  return (
    <div className="flex justify-center items-center">
      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-pink-500"></div>
      <span className="ml-3 text-gray-600">Generating recommendation...</span>
    </div>
  );
}
