export default function ProductCard({
  name,
  price,
  imgUrl,
  description,
}: {
  name: string;
  price: string;
  imgUrl: string;
  description: string;
}) {
  return (
    <div className="bg-white rounded-2xl shadow-lg flex flex-col items-center p-5">
      <img src={imgUrl} alt={name} className="w-24 h-24 object-cover rounded-xl mb-3 border border-pink-100" />
      <h3 className="text-xl font-semibold text-pink-700 mb-1">{name}</h3>
      <p className="text-sm text-pink-800 mb-2">{description}</p>
      <span className="bg-pink-200 text-pink-700 px-3 py-1 rounded-full font-bold">{price}</span>
    </div>
  );
}
